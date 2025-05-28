import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QGraphicsOpacityEffect, QFrame
from PyQt6.QtGui import QPixmap, QTransform, QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, QTimer, QUrl
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QHBoxLayout
from game.game_controller import GameController
from game.car import Direction


class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.cell_size = 30 #pixel size of cells in board
        self.setWindowTitle("ParkJamPP")
        self.setFixedSize(360, 640)  # Sets screen Size
        self.controller = GameController()
        # Locally sets parameters for the car´s board
        self.rows = self.controller.rows
        self.cols = self.controller.cols
        self.board_width = self.cols * self.cell_size
        self.board_height = self.rows * self.cell_size
        self.car_buttons = {} # Dictionary for the car images
        self.platform_widgets = {} # Dictionary for the visual widgets of the cars in the platforms
        self.init_sounds()
        self.setObjectName("MainBg")
        self.setStyleSheet("""
            #MainBg {
                background-image: url(assets/window_background.png);
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
        """)

        self.setup_ui()
        self.passenger_labels = []
        self.update_passenger_queue_display()
        self.setStyleSheet(
            "QWidget { background-image: url(assets/window_background.png); "
            "background-repeat: no-repeat; background-position: center; background-size: cover; }"
        )

    #Sets up all sound used on the project
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

    #Ensures sounds can be played on top of each other
    def play_sound(self, path: str, volume: float = 0.8):
        effect = QSoundEffect(self)  # le asignamos self como parent
        effect.setSource(QUrl.fromLocalFile(path))
        effect.setVolume(volume)
        effect.play()

        # Saves sound to avoid it getting destroyed
        if not hasattr(self, "active_sounds"):
            self.active_sounds = []

        self.active_sounds.append(effect)

        # Removes sound from the list once its over
        QTimer.singleShot(3000, lambda: self.active_sounds.remove(effect))

    def setup_ui(self):
        layout = QVBoxLayout()

        # Top part of the screen layout
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

        header_layout.addStretch()

        #  container for the reset button
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



        # Passenger queue on personalized background
        self.passenger_background = QWidget()
        self.passenger_background.setFixedSize(360, 60)
        self.passenger_background.setStyleSheet("""
            background-image: url(assets/passenger_background.png);
            background-repeat: no-repeat;
            background-position: center;
            background-size: cover;
        """)

        # Layout in background for passengers
        passenger_bg_layout = QHBoxLayout(self.passenger_background)
        passenger_bg_layout.setContentsMargins(10, 0, 10, 0)
        passenger_bg_layout.setSpacing(5)

        # Dynamic updating layout
        self.passenger_queue_layout = QHBoxLayout()
        self.passenger_queue_layout.setContentsMargins(0, 0, 0, 0)
        self.passenger_queue_layout.setSpacing(5)
        passenger_bg_layout.addLayout(self.passenger_queue_layout)

        layout.addWidget(self.passenger_background)

        # Visual container for platforms
        self.platform_container = QWidget()
        self.platform_container.setFixedSize(360, 90)
        self.platform_container.setStyleSheet(
            "background-image: url(assets/platform_background.png);"
            "background-position: center;"
            "background-size: 100% 100%;"
        )

        # Middle container to be able to center all the contents
        self.platform_layout = QHBoxLayout()
        self.platform_layout.setSpacing(0)
        self.platform_layout.setContentsMargins(5, 5, 5, 5)

        centered_layout = QHBoxLayout()
        centered_layout.addStretch(1)
        centered_layout.addLayout(self.platform_layout)
        centered_layout.addStretch(1)

        self.platform_container.setLayout(centered_layout)
        layout.addWidget(self.platform_container)

        # Car's game board
        self.board_container = QWidget()
        self.board_container.setFixedSize(360, 400)  # Puedes ajustar altura si lo deseas

        # Grass background for board area
        grass_label = QLabel(self.board_container)
        grass_label.setPixmap(QPixmap("assets/grass.png").scaled(
            360, 400,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        ))
        grass_label.setGeometry(0, 0, 360, 400)
        grass_label.lower()

        # Grid backgroung layout
        self.board_foreground = QWidget(self.board_container)
        self.board_foreground.setFixedSize(self.board_width, self.board_height)

        # Centrado horizontal y vertical dentro de board_container
        foreground_x = (360 - self.board_width) // 2
        foreground_y = (400 - self.board_height) // 2
        self.board_foreground.move(foreground_x, foreground_y)

        self.board_foreground.setStyleSheet("""
            background-image: url(assets/board_background.png);
            background-repeat: no-repeat;
            background-position: center;
            background-size: 100% 100%;
        """)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.board_foreground.setLayout(self.grid_layout)

        #Main layout
        board_wrapper = QHBoxLayout()
        board_wrapper.setContentsMargins(0, 0, 0, 0)
        board_wrapper.addStretch(1)
        board_wrapper.addWidget(self.board_container)
        board_wrapper.addStretch(1)

        layout.addLayout(board_wrapper)

        self.setLayout(layout)


        # Initialize references
        self.passenger_labels = []
        self.car_buttons = {}

        # Draw initial visual elements
        self.draw_board()
        self.update_passenger_queue_display()

    # Method responsible for updating the visual row of passengers
    # and showing animations when the front passenger has just boarded a car.
    def update_passenger_queue_display(self):

        queue = self.controller.passenger_queue.queue
        # If the queue is empty, show winning message
        if not queue:
            QMessageBox.information(self, "Well done!", "¡You win, game completed!")

        labels_existentes = getattr(self, "passenger_labels", [])

        # Checks if the passenger in front already boarded
        should_animate = False
        if labels_existentes and labels_existentes[0] and queue:
            first_color_before = labels_existentes[0].accessibleName()
            first_color_now = queue[0].color
            #Plays animation only if the next passenger is a different color
            if first_color_before != first_color_now :
                should_animate = True
                label_to_animate = labels_existentes[0]
                self.animate_passenger_boarding(label_to_animate)

        if should_animate:
            # Waits some seconds before animating
            QTimer.singleShot(300, lambda: self._refresh_passenger_queue(queue))
        else:
            self._refresh_passenger_queue(queue)

    # Logic to clean and redraw passengers on the line
    def _refresh_passenger_queue(self, queue):
        import os

        # Clean the line visually
        for i in reversed(range(self.passenger_queue_layout.count())):
            widget = self.passenger_queue_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.passenger_labels = [] # Resets the list that tracks QLabel widgets for passengers

        # Draw only the first 9 passengers on the lis by turning the queue into a list
        visible_passengers = list(queue)[:9]

        # Draws a new QLabel for each passenger and tries to assign them their image
        for passenger in visible_passengers:
            label = QLabel()
            img_path = f"assets/passengers/{passenger.color}.png"

            if not os.path.exists(img_path): # For debugging when an image is not found in the files, it would show "----"
                print(f"Imagen de pasajero no encontrada: {img_path}")
                label.setText("----")
                label.setStyleSheet(f"color: {passenger.color};")
            else: # If ian image is found it loads the image, resizes it, and puts it into the label
                pixmap = QPixmap(img_path).scaled(52, 52, Qt.AspectRatioMode.KeepAspectRatio,
                                                  Qt.TransformationMode.SmoothTransformation)
                label.setPixmap(pixmap)

            # GIves format to lavel so they are the correct size, centered and with no background
            label.setFixedSize(56, 56)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setAccessibleName(passenger.color)
            label.setStyleSheet("background: transparent;")
            self.passenger_queue_layout.addWidget(label)
            self.passenger_labels.append(label)

    #Function to debug de board
    #def debug_board(self):
        #print("Estado actual del tablero:")
        #self.controller.debug_print_board()

        # Mostrar posiciones visuales vs. lógicas para mejor depuración
        #print("\nPosiciones lógicas vs. visuales de los autos:")
        #for car in self.controller.cars:
            # Obtener celdas ocupadas por el auto según el controlador
            #cells = self.controller.get_car_cells(car)
            # Obtener posición visual para dibujar
            #visual_row, visual_col = car.get_visual_position()
            #print(f"- {car.color} ({car.capacity}): dirección {car.direction.value}")
            #print(f"  Posición lógica (cabeza): ({car.row}, {car.col})")
            #print(f"  Posición visual: ({visual_row}, {visual_col})")
            #print(f"  Celdas ocupadas: {cells}")

    # Method is responsible for rendering the entire game board: grid cells, cars, and updating platform visuals
    def draw_board(self):
        # Removes all items from the layout by iterating backwards to ensure the board starts clean
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)

        self.car_buttons = {} #Clears internal directory of caar buttons

        # Creates a visual grid on the board using placeholders in every cell
        for row in range(self.rows):
            for col in range(self.cols):
                placeholder = QLabel("")
                placeholder.setFixedSize(self.cell_size, self.cell_size)
                placeholder.setStyleSheet("border: 1px solid #999; background-color: transparent;")
                self.grid_layout.addWidget(placeholder, row, col)

        # Loops through every car in game controller
        for car in self.controller.cars:
            # Dynamically generates the path to every car´s image and skips render if the image is not found
            image_path = f"assets/cars/{car.color}car{car.capacity}.png"
            if not os.path.exists(image_path):
                print(f"Imagen no encontrada: {image_path}")
                continue

            # Loads image as pixmap
            pixmap = QPixmap(image_path)

            # Rotates the image according to the direction the car is facing
            angle = {
                Direction.UP: 0,
                Direction.RIGHT: 90,
                Direction.DOWN: 180,
                Direction.LEFT: 270,
            }.get(car.direction, 0)

            rotated_pixmap = pixmap.transformed(QTransform().rotate(angle))

            # Calculates de dimension of the image according to the direction
            width = self.cell_size if car.direction in [Direction.UP, Direction.DOWN] else self.cell_size * car.length
            height = self.cell_size * car.length if car.direction in [Direction.UP, Direction.DOWN] else self.cell_size

            # Scales the image
            scaled_pixmap = rotated_pixmap.scaled(width, height, Qt.AspectRatioMode.IgnoreAspectRatio,
                                                  Qt.TransformationMode.SmoothTransformation)

            # Creates the car button
            car_button = QPushButton()
            car_button.setIcon(QIcon(scaled_pixmap)) #Uses the cars image as the button´s icon
            # Size is set to match with the car´s scales image
            car_button.setIconSize(scaled_pixmap.size())
            car_button.setFixedSize(width, height)
            car_button.setStyleSheet("background: transparent; border: none;")
            # Clicking the car triggers try_move_car in the specific car (lambda to put that car in a loop)
            car_button.clicked.connect(lambda _, c=car: self.try_move_car(c))

            # Determines where to place the button based on the head of the car
            visual_row, visual_col = car.get_visual_position()

            # Places the button on the grid using the visual position
            self.grid_layout.addWidget(car_button, visual_row, visual_col,
                                       car.length if car.direction in [Direction.UP, Direction.DOWN] else 1, # Vertical car, spans multiple rows
                                       car.length if car.direction in [Direction.LEFT, Direction.RIGHT] else 1) # Horizontal car, spans multiple columns

            self.car_buttons[car] = car_button # Stores button reference in a dictionary so it can be accesed later

        # Updates
        self.update_platforms()

    def update_platforms(self):

        current_cars = self.controller.platform_manager.get_platform_cars() # Pulls list of cars currently in platform

        if not hasattr(self, "platform_previous_state"):
            self.platform_previous_state = {}

        # Determine which cars are gone
        new_state = {}
        old_cars = set(self.platform_widgets.keys()) #old_cars: cars from previous draw (tracked in self.platform_widgets)
        new_cars = set(current_cars) # Cars currently in platofrms
        disappeared = old_cars - new_cars # Cars that were there but disappeared

        # For every car that is ready to disappear, plays a fadeout animation but dpes not remove widget just yet
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
                self.play_sound("assets/sounds/leave_platform.wav", 0.8) # Plays sound to cue when car leaves

        # Clears widgets visually but not logically
        for i in reversed(range(self.platform_layout.count())):
            widget = self.platform_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.platform_widgets.clear()
        cars_to_remove_later = []

        # Redraws all 6 slots in the platform
        for idx in range(6):
            slot_container = QWidget()
            slot_container.setStyleSheet("background: transparent;")
            slot_container.setFixedSize(60, 80)
            slot_layout = QVBoxLayout(slot_container) # Container slots
            slot_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            slot_layout.setSpacing(2)
            slot_layout.setContentsMargins(0, 0, 0, 0)

            #If a car is found
            if idx < len(current_cars):
                car = current_cars[idx]
                # Gets image for the car dynamically
                image_path = f"assets/cars/platform_{car.color}car{car.capacity}.png"
                pixmap = QPixmap(image_path)

                # Creates a QLabel for the car image
                car_label = QLabel()
                car_label.setPixmap(pixmap)
                car_label.setFixedSize(60, 40)
                car_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                car_label.setStyleSheet("background: transparent;")

                previous = self.platform_previous_state.get(car, 0)
                current = car.boarded

                # Creates a second label to count passengers boarded
                counter_label = QLabel()
                # For when a car is fully boarded (never really got it to work)
                if car.boarded == car.capacity and previous < car.capacity:
                    counter_label.setText("DONE!")
                    counter_label.setStyleSheet("color: limegreen; font-size: 10pt; font-weight: bold;")
                    cars_to_remove_later.append((car, slot_container))
                # For when a car is not fully boarded, displays how many passengers are left
                else:
                    counter_label.setText(f"{car.boarded}/{car.capacity}")
                    counter_label.setStyleSheet("color: white; font-size: 10pt;")

                counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # Adds both labels to the layout
                slot_layout.addWidget(car_label)
                slot_layout.addWidget(counter_label)

                self.platform_layout.addWidget(slot_container)
                self.platform_widgets[car] = slot_container
                new_state[car] = current

                # Plays boarding sound only if number of passengers increased
                if current > previous:
                    self.play_sound("assets/sounds/boarding.wav", 0.6)

                # Delays car appearance so the animations can play properly
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
            else: # If spot is empty
                placeholder = QLabel() # Adds a transparent placeholder to keep alignment
                placeholder.setFixedSize(60, 40)
                placeholder.setStyleSheet("background: transparent;")
                slot_layout.addWidget(placeholder)
                self.platform_layout.addWidget(slot_container)

        # Exit animations for cars with delay
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
                    self.play_sound("assets/sounds/leave_platform.wav", 0.8) # Plays car leaving sound cue

                    def remove_widget():    #Deletes the widget
                        widget.setParent(None)
                        if car_ref in self.platform_widgets:
                            del self.platform_widgets[car_ref]

                    QTimer.singleShot(600, remove_widget)

            QTimer.singleShot(3000, animate_departure)  # Waits three seconds to animate

        self.platform_previous_state = new_state # Saves the new state of the platform

    # Attempts to move a car on a board and checks if it is possible
    def try_move_car(self, car):
        """Tries to move a car when the user clicks on it"""
        print(f"Trying to move car: {car.color} in position ({car.row}, {car.col}), and facing {car.direction}") # Prints on console which car is being moved

        # Verifies if path is clear
        path_clear = self.controller.is_path_clear(car)
        print(f"Is path clear? {path_clear}")

        # Tries to move the car
        result = self.controller.try_move_car(car)

        if result == "moved": # If no obstacles where found
            print(f"Auto {car.color} Successfully moved to platform")
            self.animate_move(car)
        elif result == "blocked": # If there was an obstacle found
            print(f"Auto {car.color} blocked, can´t move")
            self.animate_blocked(car)
        elif result == "lose": # If the platforms are full, losing and closing the game
            QMessageBox.critical(self, "Game Over!", "No more space in the platforms.")
            self.close()

    def animate_move(self, car):
        """Animates when a car exits the board"""
        button = self.car_buttons.get(car)
        if not button:
            return

        self.play_sound("assets/sounds/car_move.wav", 0.8) # Plays a sound cue to affirm a car has been set free

        # Determines the direction in which the animation will play depending on where the car is pointing
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

        # MOvement animation
        move_anim = QPropertyAnimation(button, b"pos", self)
        move_anim.setDuration(500)
        move_anim.setStartValue(button.pos())
        move_anim.setEndValue(button.pos() + QPoint(dx, dy))
        move_anim.setEasingCurve(QEasingCurve.Type.OutQuad)

        # Fade out animation
        opacity = QGraphicsOpacityEffect()
        button.setGraphicsEffect(opacity)
        fade = QPropertyAnimation(opacity, b"opacity", self)
        fade.setDuration(500)
        fade.setStartValue(1.0)
        fade.setEndValue(0.0)
        fade.setEasingCurve(QEasingCurve.Type.OutQuad)

        move_anim.start()
        fade.start()

        # Redraw board after animation
        QTimer.singleShot(500, self.draw_board)
        QTimer.singleShot(500, self.update_passenger_queue_display)

    def animate_blocked(self, car):
        """Animates a blocked car that can not move"""
        button = self.car_buttons.get(car)
        if not button:
            return

        self.play_sound("assets/sounds/error.wav", 0.8) #error sound plays

        # Shaking animation for when car is unable to move
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

        # fade out animation
        opacity = QGraphicsOpacityEffect()
        label.setGraphicsEffect(opacity)
        fade = QPropertyAnimation(opacity, b"opacity", self)
        fade.setDuration(500)
        fade.setStartValue(1.0)
        fade.setEndValue(0.0)
        fade.setEasingCurve(QEasingCurve.Type.OutQuad)

        # Movement animation
        start_pos = label.pos()
        end_pos = start_pos + QPoint(0, 20)
        move = QPropertyAnimation(label, b"pos", self)
        move.setDuration(500)
        move.setStartValue(start_pos)
        move.setEndValue(end_pos)
        move.setEasingCurve(QEasingCurve.Type.OutQuad)

        fade.start()
        move.start()

    #Redraws everything on the screen when player clicks on reset button
    def restart_game(self):
        self.controller.reset_game()
        self.draw_board()
        self.update_passenger_queue_display()
        self.update_platforms()


