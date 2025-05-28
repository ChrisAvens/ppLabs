import sys
from PyQt6.QtWidgets import QApplication
from ui.game_window import GameWindow

def main():
    app = QApplication(sys.argv) # Creates app instance
    # Initiates window and makes it visible
    window = GameWindow()
    window.show()
    # QT event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
