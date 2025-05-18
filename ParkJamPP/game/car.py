from enum import Enum
from PyQt6.QtGui import QPixmap, QTransform


class Direction(Enum):
    UP = "↑"
    DOWN = "↓"
    LEFT = "←"
    RIGHT = "→"


class Car:
    def __init__(self, color: str, capacity: int, direction: Direction, row: int, col: int):
        self.color = color
        self.capacity = capacity
        self.direction = direction
        # Posición de la cabeza del auto
        self.row = row
        self.col = col
        self.boarded = 0
        self.id = None
        self.length = self.get_length()

    def get_length(self):
        if self.capacity == 4:
            return 1
        elif self.capacity == 6:
            return 2
        elif self.capacity == 8:
            return 3
        elif self.capacity == 12:
            return 4
        return 1

    def get_sprite_path(self):
        length = self.get_length()
        dir_str = "right" if self.direction == Direction.RIGHT else "up"
        return f"assets/cars/{self.color}_{dir_str}_{length}.png"

    def get_pixmap(self):
        image_path = f"assets/car/{self.color}car{self.capacity}.png"
        pixmap = QPixmap(image_path)

        if self.direction == Direction.UP:
            return pixmap
        elif self.direction == Direction.RIGHT:
            return pixmap.transformed(QTransform().rotate(90))
        elif self.direction == Direction.DOWN:
            return pixmap.transformed(QTransform().rotate(180))
        elif self.direction == Direction.LEFT:
            return pixmap.transformed(QTransform().rotate(270))

    def get_front_position(self):
        return (self.row, self.col)

    def get_visual_position(self):
        """Retorna la posición visual para dibujar el auto en el tablero.
        Para autos hacia abajo o izquierda, ajusta la posición considerando su longitud."""
        row, col = self.row, self.col

        if self.direction == Direction.DOWN:
            # Para autos hacia abajo, no necesitamos ajuste ya que el crecimiento es positivo en filas
            pass
        elif self.direction == Direction.LEFT:
            # Para autos hacia la izquierda, ajustamos la columna para que la cabeza esté correctamente posicionada
            col = self.col - (self.length - 1)
        elif self.direction == Direction.UP:
            # Para autos hacia arriba, ajustamos la fila para que la cabeza esté correctamente posicionada
            row = self.row - (self.length - 1)
        # Para autos hacia la derecha, no necesitamos ajuste

        return row, col
