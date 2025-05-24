# game/game_controller.py

from game.car import Car, Direction
from game.platform import PlatformManager
from game.passenger import PassengerQueue
import numpy as np


class GameController:
    def __init__(self):
        self.cars = []
        self.original_cars = []  # ✅ para guardar copia original
        self.rows = 10
        self.cols = 10
        self.board_matrix = np.zeros((self.rows, self.cols), dtype=int)
        self.next_car_id = 1
        self.car_id_map = {}
        self.load_initial_data()
        self.update_board_matrix()

        self.platform_manager = PlatformManager()
        self.passenger_queue = PassengerQueue(self.cars)
        self.platform_manager.set_passenger_queue(self.passenger_queue)

        # inserting a personalized passenger list
        # yellow cars = 8 yellow passengers = 56
        # red cars = 8 red passengers = 54
        # blue cars = 6 blue passengers = 50
        # pink cars = 8 pink passengers = 50
        # green cars = 8 green passengers = 52
        # orange cars = 6 orange passengers = 42
        # passenger total = 304

        self.passenger_queue.insert_custom_queue([
            'pink', 'pink', 'pink', 'pink',
            'yellow', 'yellow', 'yellow', 'yellow',
            'blue', 'blue', 'blue',
            'red', 'red', 'red', 'red', 'red',
            'pink', 'pink', 'pink', 'pink',
            'yellow', 'yellow', 'yellow',
            'blue', 'blue', 'blue', 'blue',
            'red', 'red', 'red',
            'pink', 'pink', 'pink', 'pink',
            'yellow', 'yellow', 'yellow',
            'blue', 'blue',
            'pink', 'pink', 'pink', 'pink',
            'red', 'red', 'red',
            'green', 'green', 'green',
            'yellow', 'yellow',
            'blue', 'blue',
            'green', 'green', 'green',
            'red', 'red', 'red',
            'yellow', 'yellow', 'yellow',
            'blue', 'blue', 'blue',
            'green', 'green', 'green', 'green',
            'red', 'red', 'red',
            'yellow', 'yellow',
            'green', 'green',
            'blue', 'blue',
            'red', 'red',
            'yellow', 'yellow',
            'green', 'green', 'green',
            'blue', 'blue', 'blue',
            'red', 'red', 'red',
            'green', 'green',
            'yellow', 'yellow', 'yellow',
            'blue', 'blue',
            'green', 'green', 'green',
            'red', 'red', 'red', 'red',
            'yellow', 'yellow',
            'blue', 'blue', 'blue',
            'pink', 'pink', 'pink', 'pink', 'pink',
            'red', 'red', 'red', 'red', 'red',
            'pink', 'pink', 'pink', 'pink', 'pink', 'pink',
            'blue', 'blue', 'blue',
            'yellow', 'yellow', 'yellow', 'yellow', 'yellow',
            'green', 'green',
            'pink', 'pink', 'pink',
            'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow',
            'red', 'red', 'red',
            'blue', 'blue',
            'green', 'green', 'green',
            'red', 'red', 'red', 'red',
            'yellow', 'yellow', 'yellow', 'yellow', 'yellow',
            'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue',
            'orange', 'orange',
            'green', 'green',
            'yellow', 'yellow', 'yellow','yellow', 'yellow', 'yellow',
            'green', 'green',
            'orange', 'orange', 'orange', 'orange',
            'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red',
            'blue', 'blue', 'blue', 'blue', 'blue', 'blue',
            'yellow', 'yellow',
            'blue', 'blue', 'blue', 'blue', 'blue', 'blue',
            'yellow', 'yellow', 'yellow','yellow',
            'orange', 'orange', 'orange', 'orange',
            'yellow', 'yellow','yellow', 'yellow',
            'green', 'green', 'green',
            'red', 'red',
            'orange', 'orange',
            'green',
            'orange', 'orange', 'orange',
            'red', 'red', 'red', 'red',
            'orange', 'orange',
            'orange', 'orange', 'orange', 'orange',
            'green', 'green', 'green', 'green',
            'pink', 'pink',
            'orange', 'orange', 'orange', 'orange',
            'green', 'green', 'green', 'green',
            'orange', 'orange',
            'pink', 'pink', 'pink', 'pink', 'pink',
            'green', 'green', 'green',
            'orange', 'orange',
            'pink', 'pink', 'pink',
            'orange', 'orange', 'orange', 'orange',
            'pink', 'pink', 'pink', 'pink',
            'orange', 'orange',
            'red',
            'green', 'green', 'green', 'green',
            'orange', 'orange', 'orange', 'orange',
            'green', 'green', 'green', 'green',
            'orange', 'orange', 'orange',
            'pink', 'pink', 'pink', 'pink',
            'pink', 'pink',
        ])

    def load_initial_data(self):
        candidate_cars = [

            # 4 cell cars
            Car("red", 12, Direction.UP, 3, 9),
            Car("yellow", 12, Direction.DOWN, 5, 0),
            Car("blue", 12, Direction.RIGHT, 7, 6),
            Car("blue", 12, Direction.RIGHT, 0, 1),
            Car("pink", 12, Direction.RIGHT, 4, 5),
            Car("green", 12, Direction.LEFT, 9, 7),
            Car("orange", 12, Direction.DOWN, 5, 5),

            # 3 cell cars
            Car("yellow", 8, Direction.LEFT, 2, 4),
            Car("blue", 8, Direction.DOWN, 7, 1),
            Car("green", 8, Direction.DOWN, 4, 9),
            Car("red", 8, Direction.LEFT, 6, 4),
            Car("pink", 8, Direction.UP, 9, 3),
            Car("yellow", 8, Direction.DOWN, 1, 0),
            Car("green", 8, Direction.UP, 3, 5),
            Car("blue", 8, Direction.UP, 5, 3),
            Car("orange", 8, Direction.LEFT, 1, 4),
            Car("red", 8, Direction.DOWN, 7, 2),
            Car("pink", 8, Direction.RIGHT, 8, 6),

            #2 cell cars
            Car("blue", 6, Direction.RIGHT, 0, 7),
            Car("red", 6, Direction.DOWN, 5, 8),
            Car("yellow", 6, Direction.UP, 2, 7),
            Car("green", 6, Direction.UP, 3, 1),
            Car("yellow", 6, Direction.RIGHT, 9, 8),
            Car("red", 6, Direction.RIGHT, 0, 5),
            Car("pink", 6, Direction.LEFT, 5, 2),
            Car("orange", 6, Direction.DOWN, 7, 4),
            Car("green", 6, Direction.DOWN, 4, 4),
            Car("red", 6, Direction.LEFT, 4, 2),
            Car("orange", 6, Direction.RIGHT, 3, 6),
            Car("orange", 6, Direction.DOWN, 5, 7),
            #1 cell cars
            Car("green", 4, Direction.UP, 1, 8),
            Car("red", 4, Direction.LEFT, 9, 0),
            Car("yellow", 4, Direction.RIGHT, 3, 8),
            Car("orange", 4, Direction.LEFT, 2, 8),
            Car("blue", 4, Direction.DOWN, 4, 0),
            Car("red", 4, Direction.UP, 1, 1),
            Car("yellow", 4, Direction.DOWN, 8, 9),
            Car("pink", 4, Direction.UP, 0, 0),
            Car("pink", 4, Direction.LEFT, 3, 4),
            Car("yellow", 4, Direction.DOWN, 3, 2),
            Car("green", 4, Direction.DOWN, 6, 1),
            Car("yellow", 4, Direction.RIGHT, 1, 6),
            Car("green", 4, Direction.UP, 2, 6),
            Car("pink", 4, Direction.UP, 6, 6),
            Car("pink", 4, Direction.RIGHT, 5, 6),

        ]

        for car in candidate_cars:
            for r, c in self.get_car_cells_static(car):
                if not (0 <= r < self.rows and 0 <= c < self.cols):
                    raise ValueError(
                        f"Auto {car.color} sobresale del tablero en dirección {car.direction} desde ({car.row}, {car.col})")
            self.car_id_map[self.next_car_id] = car
            car.id = self.next_car_id
            self.next_car_id += 1
            self.cars.append(car)
            self.original_cars = [Car(car.color, car.capacity, car.direction, car.row, car.col)
                                  for car in candidate_cars]
            for c1, c2 in zip(self.original_cars, candidate_cars):
                c1.id = c2.id  # para mantener ID consistente

        self.update_board_matrix()

    def update_board_matrix(self):
        self.board_matrix = np.zeros((self.rows, self.cols), dtype=int)
        for car in self.cars:
            cells = self.get_car_cells(car)
            for row, col in cells:
                if 0 <= row < self.rows and 0 <= col < self.cols:
                    self.board_matrix[row, col] = car.id

    def get_car_cells(self, car):
        return self.get_car_cells_static(car)

    @staticmethod
    def get_car_cells_static(car):
        """Celdas que ocupa el auto desde su CABEZA hacia atrás"""
        cells = []
        for i in range(car.length):
            if car.direction == Direction.UP:
                cells.append((car.row - i, car.col))
            elif car.direction == Direction.DOWN:
                cells.append((car.row + i, car.col))
            elif car.direction == Direction.LEFT:
                cells.append((car.row, car.col - i))
            elif car.direction == Direction.RIGHT:
                cells.append((car.row, car.col + i))
        return cells

    def is_path_clear(self, car):
        car_cells = set(self.get_car_cells(car))
        path_cells = []

        if car.direction == Direction.UP:
            front_row = min(row for row, _ in car_cells)
            for r in range(front_row - 1, -1, -1):
                path_cells.append((r, car.col))

        elif car.direction == Direction.DOWN:
            front_row = max(row for row, _ in car_cells)
            for r in range(front_row + 1, self.rows):
                path_cells.append((r, car.col))

        elif car.direction == Direction.LEFT:
            front_col = min(col for _, col in car_cells)
            for c in range(front_col - 1, -1, -1):
                path_cells.append((car.row, c))

        elif car.direction == Direction.RIGHT:
            front_col = max(col for _, col in car_cells)
            for c in range(front_col + 1, self.cols):
                path_cells.append((car.row, c))

        for r, c in path_cells:
            if 0 <= r < self.rows and 0 <= c < self.cols and self.board_matrix[r, c] != 0:
                return False

        return True

    def try_move_car(self, car):
        if self.platform_manager.is_full():
            return "lose"

        if self.is_path_clear(car):
            if car in self.cars:
                self.cars.remove(car)
                self.update_board_matrix()
                self.platform_manager.add_car_to_platform(car)

                # Nuevo: permitir abordaje si hay coincidencia color al frente
                self.platform_manager.board_waiting_passengers()

                return "moved"

        return "blocked"

    def get_car_at_position(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            car_id = self.board_matrix[row, col]
            if car_id > 0:
                return self.car_id_map.get(car_id)
        return None

    def debug_print_board(self):
        print("\nEstado actual del tablero:")
        for row in range(self.rows):
            line = ""
            for col in range(self.cols):
                cell_value = self.board_matrix[row, col]
                if cell_value == 0:
                    line += ". "
                else:
                    car = self.car_id_map.get(cell_value)
                    if car:
                        line += f"{car.color[0]} "
                    else:
                        line += "? "
            print(line)
        print("Dirección de los autos:")
        for car in self.cars:
            print(f"- {car.color}: {car.direction.value} en ({car.row}, {car.col})")

    def reset_game(self):
        # Clonar autos originales
        self.cars = [Car(c.color, c.capacity, c.direction, c.original_row, c.original_col)
                     for c in self.original_cars]
        for c1, c2 in zip(self.cars, self.original_cars):
            c1.id = c2.id
            c1.original_row = c2.original_row
            c1.original_col = c2.original_col

        # Restaurar mapa e ID
        self.car_id_map = {car.id: car for car in self.cars}
        self.update_board_matrix()

        # Resetear plataformas y pasajeros
        self.platform_manager = PlatformManager()
        self.passenger_queue = PassengerQueue(self.cars)
        self.platform_manager.set_passenger_queue(self.passenger_queue)

        self.passenger_queue.insert_custom_queue([
            'pink', 'pink', 'pink', 'pink',
            'yellow', 'yellow', 'yellow', 'yellow',
            'blue', 'blue', 'blue',
            'red', 'red', 'red', 'red', 'red',
            'pink', 'pink', 'pink', 'pink',
            'yellow', 'yellow', 'yellow',
            'blue', 'blue', 'blue', 'blue',
            'red', 'red', 'red',
            'pink', 'pink', 'pink', 'pink',
            'yellow', 'yellow', 'yellow',
            'blue', 'blue',
            'pink', 'pink', 'pink', 'pink',
            'red', 'red', 'red',
            'green', 'green', 'green',
            'yellow', 'yellow',
            'blue', 'blue',
            'green', 'green', 'green',
            'red', 'red', 'red',
            'yellow', 'yellow', 'yellow',
            'blue', 'blue', 'blue',
            'green', 'green', 'green', 'green',
            'red', 'red', 'red',
            'yellow', 'yellow',
            'green', 'green',
            'blue', 'blue',
            'red', 'red',
            'yellow', 'yellow',
            'green', 'green', 'green',
            'blue', 'blue', 'blue',
            'red', 'red', 'red',
            'green', 'green',
            'yellow', 'yellow', 'yellow',
            'blue', 'blue',
            'green', 'green', 'green',
            'red', 'red', 'red', 'red',
            'yellow', 'yellow',
            'blue', 'blue', 'blue',
            'pink', 'pink', 'pink', 'pink', 'pink',
            'red', 'red', 'red', 'red', 'red',
            'pink', 'pink', 'pink', 'pink', 'pink', 'pink',
            'blue', 'blue', 'blue',
            'yellow', 'yellow', 'yellow', 'yellow', 'yellow',
            'green', 'green',
            'pink', 'pink', 'pink',
            'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow',
            'red', 'red', 'red',
            'blue', 'blue',
            'green', 'green', 'green',
            'red', 'red', 'red', 'red',
            'yellow', 'yellow', 'yellow', 'yellow', 'yellow',
            'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue',
            'orange', 'orange',
            'green', 'green',
            'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow',
            'green', 'green',
            'orange', 'orange', 'orange', 'orange',
            'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red',
            'blue', 'blue', 'blue', 'blue', 'blue', 'blue',
            'yellow', 'yellow',
            'blue', 'blue', 'blue', 'blue', 'blue', 'blue',
            'yellow', 'yellow', 'yellow', 'yellow',
            'orange', 'orange', 'orange', 'orange',
            'yellow', 'yellow', 'yellow', 'yellow',
            'green', 'green', 'green',
            'red', 'red',
            'orange', 'orange',
            'green',
            'orange', 'orange', 'orange',
            'red', 'red', 'red', 'red',
            'orange', 'orange',
            'orange', 'orange', 'orange', 'orange',
            'green', 'green', 'green', 'green',
            'pink', 'pink',
            'orange', 'orange', 'orange', 'orange',
            'green', 'green', 'green', 'green',
            'orange', 'orange',
            'pink', 'pink', 'pink', 'pink', 'pink',
            'green', 'green', 'green',
            'orange', 'orange',
            'pink', 'pink', 'pink',
            'orange', 'orange', 'orange', 'orange',
            'pink', 'pink', 'pink', 'pink',
            'orange', 'orange',
            'red',
            'green', 'green', 'green', 'green',
            'orange', 'orange', 'orange', 'orange',
            'green', 'green', 'green', 'green',
            'orange', 'orange', 'orange',
            'pink', 'pink', 'pink', 'pink',
            'pink', 'pink',
        ])

