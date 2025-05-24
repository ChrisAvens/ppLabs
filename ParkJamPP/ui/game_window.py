import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QGraphicsOpacityEffect, QFrame
from PyQt6.QtGui import QFont, QPixmap, QTransform, QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, QTimer, QUrl
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QHBoxLayout
from game.game_controller import GameController
from game.car import Direction


class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.cell_size = 30
        self.setWindowTitle("ParkJamPP")
        self.setFixedSize(360, 640)  # Tamaño vertical estilo móvil
        self.controller = GameController()
        self.rows = self.controller.rows
        self.cols = self.controller.cols
        self.board_width = self.cols * self.cell_size
        self.board_height = self.rows * self.cell_size
        self.car_buttons = {}
        self.platform_widgets = {}  # key: car, value: widget
        self.init_sounds()
        # -- Fondo global sólo para este widget raíz --
        self.setObjectName("MainBg")  # ① le ponemos un id único
        self.setStyleSheet("""
            #MainBg {                         /* ② se aplica SÓLO a este objeto */
                background-image: url(assets/window_background.png);
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
        """)

        self.setup_ui()
        self.passenger_labels = []  # Guardaremos referencias para actualizarlas fácilmente
        self.update_passenger_queue_display()
        self.setStyleSheet(
            "QWidget { background-image: url(assets/window_background.png); "
            "background-repeat: no-repeat; background-position: center; background-size: cover; }"
        )

    def init_sounds(self):
        self.sound_move = QSoundEffect()
        self.sound_move.setSource(QUrl.fromLocalFile("assets/sounds/car_move.wav"))
        self.sound_move.setVolume(0.6)

        self.sound_error = QSoundEffect()
        self.sound_error.setSource(QUrl.fromLocalFile("assets/sounds/error.wav"))
        self.sound_error.setVolume(0.6)

        self.sound_leave = QSoundEffect()
        self.sound_leave.setSource(QUrl.fromLocalFile("assets/sounds/leave_platform.wav"))
        self.sound_leave.setVolume(0.8)

        self.sound_leave = QSoundEffect()
        self.sound_leave.setSource(QUrl.fromLocalFile("assets/sounds/boarding.wav"))
        self.sound_leave.setVolume(0.8)

    def play_sound(self, path: str, volume: float = 0.8):
        effect = QSoundEffect(self)  # le asignamos self como parent
        effect.setSource(QUrl.fromLocalFile(path))
        effect.setVolume(volume)
        effect.play()

        # Guardar el sonido para que no sea destruido
        if not hasattr(self, "active_sounds"):
            self.active_sounds = []

        self.active_sounds.append(effect)

        # Eliminar el sonido de la lista cuando termine (aproximadamente)
        QTimer.singleShot(3000, lambda: self.active_sounds.remove(effect))

    def setup_ui(self):
        layout = QVBoxLayout()

        # --- ENCABEZADO CON IMAGEN Y BOTÓN AISLADO ---
        self.header_section = QFrame()
        self.header_section.setFixedSize(360, 80)
        self.header_section.setStyleSheet("""
            background-image: url(assets/title.png);
            background-repeat: no-repeat;
            background-position: center;
            background-size: cover;
        """)

        header_layout = QHBoxLayout(self.header_section)
        header_layout.setContentsMargins(10, 0, 10, 0)
        header_layout.setSpacing(10)

        # Espaciador
        header_layout.addStretch()

        # Contenedor del botón (sin heredar fondo)
        reset_container = QWidget()
        reset_container.setStyleSheet("background: transparent;")
        reset_layout = QVBoxLayout(reset_container)
        reset_layout.setContentsMargins(0, 0, 0, 0)
        reset_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)

        reset_button = QPushButton("Reiniciar")
        reset_button.setFixedSize(120, 40)
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #730404;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                background-image: none;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        reset_button.clicked.connect(self.restart_game)
        reset_layout.addWidget(reset_button)

        header_layout.addWidget(reset_container)
        layout.addWidget(self.header_section)



        # 3. Fila de pasajeros dentro de fondo personalizado
        self.passenger_background = QWidget()
        self.passenger_background.setFixedSize(360, 60)
        self.passenger_background.setStyleSheet("""
            background-image: url(assets/passenger_background.png);
            background-repeat: no-repeat;
            background-position: center;
            background-size: cover;
        """)

        # Layout dentro del fondo (para los pasajeros)
        passenger_bg_layout = QHBoxLayout(self.passenger_background)
        passenger_bg_layout.setContentsMargins(10, 0, 10, 0)
        passenger_bg_layout.setSpacing(5)

        # Este layout es el que se va a actualizar dinámicamente
        self.passenger_queue_layout = QHBoxLayout()
        self.passenger_queue_layout.setContentsMargins(0, 0, 0, 0)
        self.passenger_queue_layout.setSpacing(5)

        # Agregamos el layout real dentro del contenedor con fondo
        passenger_bg_layout.addLayout(self.passenger_queue_layout)

        # Finalmente, agregamos el contenedor al layout principal
        layout.addWidget(self.passenger_background)

        # 4. Contenedor visual de plataformas (centrado)
        self.platform_container = QWidget()
        self.platform_container.setFixedSize(360, 90)
        self.platform_container.setStyleSheet(
            "background-image: url(assets/platform_background.png);"
            "background-position: center;"
            "background-size: 100% 100%;"
        )

        # Contenedor intermedio para centrar el contenido
        self.platform_layout = QHBoxLayout()
        self.platform_layout.setSpacing(0)
        self.platform_layout.setContentsMargins(5, 5, 5, 5)

        centered_layout = QHBoxLayout()
        centered_layout.addStretch(1)
        centered_layout.addLayout(self.platform_layout)
        centered_layout.addStretch(1)

        self.platform_container.setLayout(centered_layout)
        layout.addWidget(self.platform_container)

        # --- TABLERO VISUAL CON FONDOS Y CUADRÍCULA ---
        self.board_container = QWidget()
        self.board_container.setFixedSize(360, 400)  # Puedes ajustar altura si lo deseas

        # Capa 0: fondo GRASS para todo el área del tablero
        grass_label = QLabel(self.board_container)
        grass_label.setPixmap(QPixmap("assets/grass.png").scaled(
            360, 400,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        ))
        grass_label.setGeometry(0, 0, 360, 400)
        grass_label.lower()

        # Capa 1: contenedor del tablero (solo el área del fondo de la cuadrícula)
        self.board_foreground = QWidget(self.board_container)
        self.board_foreground.setFixedSize(self.board_width, self.board_height)

        # Centrado horizontal y vertical dentro de board_container
        foreground_x = (360 - self.board_width) // 2
        foreground_y = (400 - self.board_height) // 2
        self.board_foreground.move(foreground_x, foreground_y)

        # Fondo del tablero dentro del área exacta
        self.board_foreground.setStyleSheet("""
            background-image: url(assets/board_background.png);
            background-repeat: no-repeat;
            background-position: center;
            background-size: 100% 100%;
        """)

        # Layout de cuadrícula sobre el fondo
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.board_foreground.setLayout(self.grid_layout)

        # Finalmente añadimos al layout principal
        board_wrapper = QHBoxLayout()
        board_wrapper.setContentsMargins(0, 0, 0, 0)
        board_wrapper.addStretch(1)
        board_wrapper.addWidget(self.board_container)
        board_wrapper.addStretch(1)

        layout.addLayout(board_wrapper)


        # Finalizar
        self.setLayout(layout)


        # Inicializar referencias
        self.passenger_labels = []
        self.car_buttons = {}

        # Dibujar elementos visuales iniciales
        self.draw_board()
        self.update_passenger_queue_display()

    def update_passenger_queue_display(self):
        import os

        queue = self.controller.passenger_queue.queue
        # Si la fila está vacía y el juego sigue, mostrar mensaje de victoria
        if not queue:
            QMessageBox.information(self, "¡Victoria!", "¡Ganaste, juego completado!")

        labels_existentes = getattr(self, "passenger_labels", [])

        # Checar si el pasajero al frente cambió (se abordó)
        should_animate = False
        if labels_existentes and labels_existentes[0] and queue:
            first_color_before = labels_existentes[0].accessibleName()
            first_color_now = queue[0].color
            if first_color_before != first_color_now:
                should_animate = True
                label_to_animate = labels_existentes[0]
                self.animate_passenger_boarding(label_to_animate)

        if should_animate:
            # Esperar 600 ms para dejar que se vea la animación antes de refrescar
            QTimer.singleShot(600, lambda: self._refresh_passenger_queue(queue))
        else:
            self._refresh_passenger_queue(queue)

    def _refresh_passenger_queue(self, queue):
        import os

        # Limpiar visualmente la fila
        for i in reversed(range(self.passenger_queue_layout.count())):
            widget = self.passenger_queue_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.passenger_labels = []

        # Solo mostrar los primeros 9 pasajeros
        visible_passengers = list(queue)[:9]

        for passenger in visible_passengers:
            label = QLabel()
            img_path = f"assets/passengers/{passenger.color}.png"

            if not os.path.exists(img_path):
                print(f"⚠ Imagen de pasajero no encontrada: {img_path}")
                label.setText("👤")
                label.setStyleSheet(f"color: {passenger.color};")
            else:
                pixmap = QPixmap(img_path).scaled(52, 52, Qt.AspectRatioMode.KeepAspectRatio,
                                                  Qt.TransformationMode.SmoothTransformation)
                label.setPixmap(pixmap)

            label.setFixedSize(56, 56)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setAccessibleName(passenger.color)
            label.setStyleSheet("background: transparent;")
            self.passenger_queue_layout.addWidget(label)
            self.passenger_labels.append(label)

    def debug_board(self):
        """Función de depuración para imprimir el estado del tablero"""
        print("Estado actual del tablero:")
        self.controller.debug_print_board()

        # Mostrar posiciones visuales vs. lógicas para mejor depuración
        print("\nPosiciones lógicas vs. visuales de los autos:")
        for car in self.controller.cars:
            # Obtener celdas ocupadas por el auto según el controlador
            cells = self.controller.get_car_cells(car)
            # Obtener posición visual para dibujar
            visual_row, visual_col = car.get_visual_position()
            print(f"- {car.color} ({car.capacity}): dirección {car.direction.value}")
            print(f"  Posición lógica (cabeza): ({car.row}, {car.col})")
            print(f"  Posición visual: ({visual_row}, {visual_col})")
            print(f"  Celdas ocupadas: {cells}")

    def draw_board(self):
        # Limpiar el tablero actual
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)

        self.car_buttons = {}

        # Colocar placeholders en cada celda
        for row in range(self.rows):
            for col in range(self.cols):
                placeholder = QLabel("")
                placeholder.setFixedSize(self.cell_size, self.cell_size)
                placeholder.setStyleSheet("border: 1px solid #999; background-color: transparent;")
                self.grid_layout.addWidget(placeholder, row, col)

        # Dibujar los autos
        for car in self.controller.cars:
            # Obtener la imagen del auto
            image_path = f"assets/cars/{car.color}car{car.capacity}.png"
            if not os.path.exists(image_path):
                print(f"⚠ Imagen no encontrada: {image_path}")
                continue

            pixmap = QPixmap(image_path)

            # Rotar la imagen según la dirección
            angle = {
                Direction.UP: 0,
                Direction.RIGHT: 90,
                Direction.DOWN: 180,
                Direction.LEFT: 270,
            }.get(car.direction, 0)

            rotated_pixmap = pixmap.transformed(QTransform().rotate(angle))

            # Calcular dimensiones según la dirección
            width = self.cell_size if car.direction in [Direction.UP, Direction.DOWN] else self.cell_size * car.length
            height = self.cell_size * car.length if car.direction in [Direction.UP, Direction.DOWN] else self.cell_size

            # Escalar la imagen
            scaled_pixmap = rotated_pixmap.scaled(width, height, Qt.AspectRatioMode.IgnoreAspectRatio,
                                                  Qt.TransformationMode.SmoothTransformation)

            # Crear botón del auto
            car_button = QPushButton()
            car_button.setIcon(QIcon(scaled_pixmap))
            car_button.setIconSize(scaled_pixmap.size())
            car_button.setFixedSize(width, height)
            car_button.setStyleSheet("background: transparent; border: none;")
            car_button.clicked.connect(lambda _, c=car: self.try_move_car(c))

            # Obtener la posición visual para el dibujado
            visual_row, visual_col = car.get_visual_position()

            # Posicionar el botón en el grid usando la posición visual
            self.grid_layout.addWidget(car_button, visual_row, visual_col,
                                       car.length if car.direction in [Direction.UP, Direction.DOWN] else 1,
                                       car.length if car.direction in [Direction.LEFT, Direction.RIGHT] else 1)

            self.car_buttons[car] = car_button

        # Actualizar plataformas
        self.update_platforms()

    def update_platforms(self):
        from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget
        from PyQt6.QtCore import QPropertyAnimation, QTimer, QPoint
        from PyQt6.QtWidgets import QGraphicsOpacityEffect

        current_cars = self.controller.platform_manager.get_platform_cars()

        if not hasattr(self, "platform_previous_state"):
            self.platform_previous_state = {}

        new_state = {}
        old_cars = set(self.platform_widgets.keys())
        new_cars = set(current_cars)
        disappeared = old_cars - new_cars

        # Autos que se fueron naturalmente
        for car in disappeared:
            widget = self.platform_widgets.get(car)
            if widget:
                opacity = QGraphicsOpacityEffect()
                widget.setGraphicsEffect(opacity)
                fade = QPropertyAnimation(opacity, b"opacity", self)
                fade.setDuration(400)
                fade.setStartValue(1.0)
                fade.setEndValue(0.0)
                fade.setEasingCurve(QEasingCurve.Type.OutCubic)
                fade.start()
                self.play_sound("assets/sounds/leave_platform.wav", 0.8)

        # Limpiar visual pero mantener lógica
        for i in reversed(range(self.platform_layout.count())):
            widget = self.platform_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.platform_widgets.clear()
        cars_to_remove_later = []

        for idx in range(6):
            slot_container = QWidget()
            slot_container.setStyleSheet("background: transparent;")
            slot_container.setFixedSize(60, 80)
            slot_layout = QVBoxLayout(slot_container)
            slot_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            slot_layout.setSpacing(2)
            slot_layout.setContentsMargins(0, 0, 0, 0)

            if idx < len(current_cars):
                car = current_cars[idx]
                image_path = f"assets/cars/platform_{car.color}car{car.capacity}.png"
                pixmap = QPixmap(image_path)

                car_label = QLabel()
                car_label.setPixmap(pixmap)
                car_label.setFixedSize(60, 40)
                car_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                car_label.setStyleSheet("background: transparent;")

                previous = self.platform_previous_state.get(car, 0)
                current = car.boarded

                # Mostrar contador o DONE!
                counter_label = QLabel()
                if car.boarded == car.capacity and previous < car.capacity:
                    counter_label.setText("DONE! ✅")
                    counter_label.setStyleSheet("color: limegreen; font-size: 10pt; font-weight: bold;")
                    cars_to_remove_later.append((car, slot_container))
                else:
                    counter_label.setText(f"{car.boarded}/{car.capacity}")
                    counter_label.setStyleSheet("color: white; font-size: 10pt;")

                counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                slot_layout.addWidget(car_label)
                slot_layout.addWidget(counter_label)

                self.platform_layout.addWidget(slot_container)
                self.platform_widgets[car] = slot_container
                new_state[car] = current

                if current > previous:
                    self.play_sound("assets/sounds/boarding.wav", 0.6)

                if car not in old_cars:
                    def animate_appearance(widget=slot_container):
                        opacity = QGraphicsOpacityEffect()
                        widget.setGraphicsEffect(opacity)
                        opacity.setOpacity(0.0)

                        fade_in = QPropertyAnimation(opacity, b"opacity", self)
                        fade_in.setDuration(400)
                        fade_in.setStartValue(0.0)
                        fade_in.setEndValue(1.0)
                        fade_in.setEasingCurve(QEasingCurve.Type.OutCubic)
                        fade_in.start()

                        start_pos = widget.pos() + QPoint(0, 20)
                        end_pos = widget.pos()
                        widget.move(start_pos)

                        anim_pos = QPropertyAnimation(widget, b"pos", self)
                        anim_pos.setDuration(400)
                        anim_pos.setStartValue(start_pos)
                        anim_pos.setEndValue(end_pos)
                        anim_pos.setEasingCurve(QEasingCurve.Type.OutCubic)
                        anim_pos.start()

                    QTimer.singleShot(1, animate_appearance)
            else:
                placeholder = QLabel()
                placeholder.setFixedSize(60, 40)
                placeholder.setStyleSheet("background: transparent;")
                slot_layout.addWidget(placeholder)
                self.platform_layout.addWidget(slot_container)

        # Animaciones de salida para autos llenos (espera 3 segundos)
        for car, widget_ref in cars_to_remove_later:
            def animate_departure(car_ref=car, widget=widget_ref):
                if car_ref in self.platform_widgets:
                    opacity = QGraphicsOpacityEffect()
                    widget.setGraphicsEffect(opacity)

                    fade = QPropertyAnimation(opacity, b"opacity", self)
                    fade.setDuration(500)
                    fade.setStartValue(1.0)
                    fade.setEndValue(0.0)
                    fade.setEasingCurve(QEasingCurve.Type.InCubic)

                    start_pos = widget.pos()
                    end_pos = start_pos + QPoint(0, 20)

                    anim_pos = QPropertyAnimation(widget, b"pos", self)
                    anim_pos.setDuration(500)
                    anim_pos.setStartValue(start_pos)
                    anim_pos.setEndValue(end_pos)
                    anim_pos.setEasingCurve(QEasingCurve.Type.InCubic)

                    fade.start()
                    anim_pos.start()
                    self.play_sound("assets/sounds/leave_platform.wav", 0.8)

                    def remove_widget():
                        widget.setParent(None)
                        if car_ref in self.platform_widgets:
                            del self.platform_widgets[car_ref]

                    QTimer.singleShot(600, remove_widget)

            QTimer.singleShot(3000, animate_departure)  # 🕒 ¡Ahora espera 3 segundos!

        self.platform_previous_state = new_state

    def try_move_car(self, car):
        """Intenta mover un auto cuando el usuario hace clic en él"""
        print(f"Intentando mover auto: {car.color} en posición ({car.row}, {car.col}), dirección {car.direction}")

        # Verificar si el camino está libre
        path_clear = self.controller.is_path_clear(car)
        print(f"¿Camino libre? {path_clear}")

        # Intentar mover el auto
        result = self.controller.try_move_car(car)

        if result == "moved":
            print(f"Auto {car.color} movido exitosamente a la plataforma")
            self.animate_move(car)
        elif result == "blocked":
            print(f"Auto {car.color} bloqueado, no puede moverse")
            self.animate_blocked(car)
        elif result == "lose":
            QMessageBox.critical(self, "¡Juego terminado!", "Ya no hay espacio en las plataformas. Perdiste.")
            self.close()

    def animate_move(self, car):
        """Anima la salida del auto del tablero"""
        button = self.car_buttons.get(car)
        if not button:
            return

        self.play_sound("assets/sounds/car_move.wav", 0.8)

        # Determinar dirección de movimiento según la dirección del auto
        dx, dy = 0, 0
        offset = 150
        if car.direction == Direction.UP:
            dy = -offset
        elif car.direction == Direction.DOWN:
            dy = offset
        elif car.direction == Direction.LEFT:
            dx = -offset
        elif car.direction == Direction.RIGHT:
            dx = offset

        # Animación de movimiento
        move_anim = QPropertyAnimation(button, b"pos", self)
        move_anim.setDuration(500)
        move_anim.setStartValue(button.pos())
        move_anim.setEndValue(button.pos() + QPoint(dx, dy))
        move_anim.setEasingCurve(QEasingCurve.Type.OutQuad)

        # Animación de desvanecimiento
        opacity = QGraphicsOpacityEffect()
        button.setGraphicsEffect(opacity)
        fade = QPropertyAnimation(opacity, b"opacity", self)
        fade.setDuration(500)
        fade.setStartValue(1.0)
        fade.setEndValue(0.0)
        fade.setEasingCurve(QEasingCurve.Type.OutQuad)

        move_anim.start()
        fade.start()

        # Redibujar el tablero después de la animación
        QTimer.singleShot(500, self.draw_board)
        QTimer.singleShot(500, self.update_passenger_queue_display)

    def animate_blocked(self, car):
        """Anima un auto bloqueado que no puede moverse"""
        button = self.car_buttons.get(car)
        if not button:
            return

        self.play_sound("assets/sounds/error.wav", 0.8)

        # Animación de "temblor" para indicar que está bloqueado
        original_pos = button.pos()
        shake_anim = QPropertyAnimation(button, b"pos", self)
        shake_anim.setDuration(300)
        shake_anim.setKeyValueAt(0.0, original_pos)
        shake_anim.setKeyValueAt(0.1, original_pos + QPoint(-5, 0))
        shake_anim.setKeyValueAt(0.2, original_pos + QPoint(5, 0))
        shake_anim.setKeyValueAt(0.3, original_pos + QPoint(-5, 0))
        shake_anim.setKeyValueAt(0.4, original_pos + QPoint(5, 0))
        shake_anim.setKeyValueAt(0.5, original_pos + QPoint(-5, 0))
        shake_anim.setKeyValueAt(0.6, original_pos + QPoint(5, 0))
        shake_anim.setKeyValueAt(0.7, original_pos + QPoint(-5, 0))
        shake_anim.setKeyValueAt(0.8, original_pos + QPoint(5, 0))
        shake_anim.setKeyValueAt(0.9, original_pos + QPoint(-5, 0))
        shake_anim.setKeyValueAt(1.0, original_pos)
        shake_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        shake_anim.start()

    def animate_passenger_boarding(self, label: QLabel):
        if not label:
            return

        # Animación de desvanecimiento
        opacity = QGraphicsOpacityEffect()
        label.setGraphicsEffect(opacity)
        fade = QPropertyAnimation(opacity, b"opacity", self)
        fade.setDuration(500)
        fade.setStartValue(1.0)
        fade.setEndValue(0.0)
        fade.setEasingCurve(QEasingCurve.Type.OutQuad)

        # Animación de bajada
        start_pos = label.pos()
        end_pos = start_pos + QPoint(0, 20)
        move = QPropertyAnimation(label, b"pos", self)
        move.setDuration(500)
        move.setStartValue(start_pos)
        move.setEndValue(end_pos)
        move.setEasingCurve(QEasingCurve.Type.OutQuad)

        fade.start()
        move.start()

    def restart_game(self):
        self.controller.reset_game()
        self.draw_board()  # 🔁 Recoloca los autos en el tablero
        self.update_passenger_queue_display()
        self.update_platforms()


