import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QMessageBox, QGraphicsOpacityEffect
from PyQt6.QtGui import QFont, QPixmap, QTransform, QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, QTimer, QUrl
from PyQt6.QtMultimedia import QSoundEffect
from game.game_controller import GameController
from game.car import Direction


class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.cell_size = 60
        self.setWindowTitle("ParkJamPP")
        self.controller = GameController()
        self.rows = self.controller.rows
        self.cols = self.controller.cols
        self.board_width = self.cols * self.cell_size
        self.board_height = self.rows * self.cell_size
        self.car_buttons = {}
        self.init_sounds()
        self.setup_ui()
        self.setStyleSheet(
            "QWidget { background-image: url(assets/window_background.png); "
            "background-repeat: no-repeat; background-position: center; background-size: cover; }"
        )

    def init_sounds(self):
        self.sound_move = QSoundEffect()
        self.sound_move.setSource(QUrl.fromLocalFile("assets/sounds/car_move.wav"))
        self.sound_move.setVolume(0.5)

        self.sound_error = QSoundEffect()
        self.sound_error.setSource(QUrl.fromLocalFile("assets/sounds/error.wav"))
        self.sound_error.setVolume(0.8)

    def setup_ui(self):
        layout = QVBoxLayout()
        title = QLabel("ParkJam - Tablero con fondo")
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Agregar botón para imprimir estado del tablero (depuración)
        debug_button = QPushButton("Depurar Tablero")
        debug_button.clicked.connect(self.debug_board)
        layout.addWidget(debug_button)

        self.board_container = QWidget()
        self.board_container.setFixedSize(self.board_width, self.board_height)
        self.board_container.setStyleSheet(
            "background-image: url(assets/board_background.png);"
            "background-repeat: no-repeat;"
            "background-position: center;"
            "background-size: cover;"
        )

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.board_container.setLayout(self.grid_layout)
        layout.addWidget(self.board_container)

        layout.addWidget(QLabel("🅿️ Plataformas (máx 6 autos):"))
        self.platform_labels = QGridLayout()
        layout.addLayout(self.platform_labels)

        self.setLayout(layout)
        self.draw_board()
        self.adjustSize()

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
            scaled_pixmap = rotated_pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio,
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
        """Actualiza la visualización de las plataformas con los autos actuales"""
        # Limpiar plataformas actuales
        for i in reversed(range(self.platform_labels.count())):
            self.platform_labels.itemAt(i).widget().setParent(None)

        # Mostrar autos en plataformas
        for idx, car in enumerate(self.controller.platforms):
            label = QLabel(f"{car.color} ({car.capacity})")
            label.setStyleSheet(f"background-color: {car.color}; color: white; padding: 5px;")
            label.setFixedSize(100, 30)
            self.platform_labels.addWidget(label, 0, idx)

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

        self.sound_move.play()

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

    def animate_blocked(self, car):
        """Anima un auto bloqueado que no puede moverse"""
        button = self.car_buttons.get(car)
        if not button:
            return

        self.sound_error.play()

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
