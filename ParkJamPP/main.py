import sys
from PyQt6.QtWidgets import QApplication
from ui.game_window import GameWindow

def main():
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
