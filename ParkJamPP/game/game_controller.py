from game.car import Car, Direction

class GameController:
    def __init__(self):
        self.cars = []
        self.platforms = []
        self.max_platforms = 6
        self.rows = 8
        self.cols = 6

    def load_initial_data(self):
        self.cars = [
            Car("red", 4, Direction.UP, 3, 1),
            Car("blue", 6, Direction.DOWN, 1, 0),
            Car("green", 8, Direction.RIGHT, 6, 0),
            Car("yellow", 12, Direction.LEFT, 1, 5)
        ]

    def get_car_at(self, row, col):
        for car in self.cars:
            for i in range(car.length):
                r, c = car.row, car.col
                if car.direction in [Direction.UP, Direction.DOWN]:
                    r = car.row + i if car.direction == Direction.DOWN else car.row - i
                else:
                    c = car.col + i if car.direction == Direction.RIGHT else car.col - i
                if r == row and c == col:
                    return car
        return None

    def is_path_clear(self, car: Car):
        length = car.length
        if car.direction == Direction.UP:
            for i in range(1, car.row + 1):
                if self.get_car_at(car.row - i, car.col):
                    return False
            return car.row - length >= 0
        elif car.direction == Direction.DOWN:
            for i in range(1, self.rows - (car.row + length - 1)):
                if self.get_car_at(car.row + length - 1 + i, car.col):
                    return False
            return car.row + length - 1 < self.rows
        elif car.direction == Direction.LEFT:
            for i in range(1, car.col + 1):
                if self.get_car_at(car.row, car.col - i):
                    return False
            return car.col - length + 1 >= 0
        elif car.direction == Direction.RIGHT:
            for i in range(1, self.cols - (car.col + length - 1)):
                if self.get_car_at(car.row, car.col + length - 1 + i):
                    return False
            return car.col + length <= self.cols
        return False

    def try_move_car(self, car: Car):
        if len(self.platforms) >= self.max_platforms:
            return "lose"
        if self.is_path_clear(car):
            if car in self.cars:
                self.cars.remove(car)
                self.platforms.append(car)
                return "moved"
        return "blocked"
