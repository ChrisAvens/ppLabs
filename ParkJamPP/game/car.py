from enum import Enum

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
        self.row = row
        self.col = col
        self.boarded = 0
        self.length = self.get_length()

        max_rows, max_cols = 8, 6
        if self.direction == Direction.RIGHT and col + self.length > max_cols:
            raise ValueError("Auto sobresale del tablero hacia la derecha.")
        if self.direction == Direction.LEFT and col - self.length + 1 < 0:
            raise ValueError("Auto sobresale del tablero hacia la izquierda.")
        if self.direction == Direction.DOWN and row + self.length > max_rows:
            raise ValueError("Auto sobresale del tablero hacia abajo.")
        if self.direction == Direction.UP and row - self.length + 1 < 0:
            raise ValueError("Auto sobresale del tablero hacia arriba.")

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
