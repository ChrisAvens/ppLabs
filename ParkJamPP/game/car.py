from enum import Enum
from PyQt6.QtGui import QPixmap, QTransform

# Defines the directions in which de cars can go
class Direction(Enum):
    UP = "↑"
    DOWN = "↓"
    LEFT = "←"
    RIGHT = "→"

#Creates a new car with color, direction, capacity and stores the value of its original position in the board
class Car:
    def __init__(self, color: str, capacity: int, direction: Direction, row: int, col: int):
        self.color = color
        self.capacity = capacity
        self.direction = direction
        # position
        self.row = row
        self.col = col
        # original position for restart button
        self.original_row = row
        self.original_col = col
        self.boarded = 0 #for counting passsengers that have boarded
        self.id = None #ID to identify car in the board matrix
        self.length = self.get_length() #for visual length

    #Defines the lenght of the vehicle according to its capacity
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

    #gets the path for the picture of the car according to its color and capacity
    def get_sprite_path(self):
        length = self.get_length()
        dir_str = "right" if self.direction == Direction.RIGHT else "up"
        return f"assets/cars/{self.color}_{length}.png"


    #rotates the images of the cars to the direction in which they are able to move
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

    #Returns the position of the front of the car to calculate collitions and accurately draw the cars
    def get_front_position(self):
        return (self.row, self.col)


    #Calculates how will tha cars be drawn in the board to ensure its the same way as visually represented
    def get_visual_position(self):
        """Returns the visual position to draw the car on the board.
        For cars going up or left, adjusts the position taking its length in mind."""
        row, col = self.row, self.col

        if self.direction == Direction.DOWN:
            pass
        elif self.direction == Direction.LEFT:
            # For cars going left, we adjust the column to ensure its drawn properly
            col = self.col - (self.length - 1)
        elif self.direction == Direction.UP:
            # For cars going up, we adjust the row to ensure its drawn properly
            row = self.row - (self.length - 1)

        return row, col
