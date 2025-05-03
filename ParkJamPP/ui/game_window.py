from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from game.game_controller import GameController

class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ParkJamPP")
        self.setMinimumSize(800, 700)
        self.controller = GameController()
        self.controller.load_initial_data()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setStyleSheet("background-color: lightgreen;")
        title = QLabel("ParkJam - Test 1")
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self.grid_layout)

        layout.addWidget(QLabel("🅿️ Plataformas (máx 6 autos):"))
        self.platform_labels = QGridLayout()
        layout.addLayout(self.platform_labels)

        self.setLayout(layout)
        self.draw_board()

    def draw_board(self):
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)

        # Fondo gris para tablero
        for row in range(self.controller.rows):
            for col in range(self.controller.cols):
                placeholder = QLabel("")
                placeholder.setFixedSize(48, 48)
                placeholder.setStyleSheet("border: 1px solid #999; background-color: #ccc;")
                self.grid_layout.addWidget(placeholder, row, col)

        for car in self.controller.cars:
            for i in range(car.length):
                r, c = car.row, car.col
                if car.direction.name in ["UP", "DOWN"]:
                    r = car.row + i if car.direction.name == "DOWN" else car.row - i
                else:
                    c = car.col + i if car.direction.name == "RIGHT" else car.col - i

                car_btn = QPushButton(f"{car.capacity}\n{car.direction.value}")
                car_btn.setFixedSize(48, 48)
                car_btn.setStyleSheet(f"background-color: {car.color}; color: white; font-weight: bold;")
                car_btn.clicked.connect(lambda _, c=car: self.try_move_car(c))
                self.grid_layout.addWidget(car_btn, r, c)

        self.update_platforms()

    def update_platforms(self):
        for i in reversed(range(self.platform_labels.count())):
            self.platform_labels.itemAt(i).widget().setParent(None)

        for idx, car in enumerate(self.controller.platforms):
            label = QLabel(f"{car.color} ({car.capacity})")
            label.setStyleSheet(f"background-color: {car.color}; color: white; padding: 5px;")
            label.setFixedSize(100, 30)
            self.platform_labels.addWidget(label, 0, idx)

    def try_move_car(self, car):
        result = self.controller.try_move_car(car)
        if result == "moved":
            self.draw_board()
        elif result == "blocked":
            QMessageBox.information(self, "No se puede mover", "Este auto está bloqueado.")
        elif result == "lose":
            QMessageBox.critical(self, "¡Juego terminado!", "Ya no hay espacio en las plataformas. Perdiste.")
            self.close()
