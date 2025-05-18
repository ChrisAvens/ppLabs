from game.car import Car, Direction
import numpy as np


class GameController:
    def __init__(self):
        self.cars = []
        self.platforms = []
        self.max_platforms = 6
        self.rows = 10
        self.cols = 10
        self.board_matrix = np.zeros((self.rows, self.cols), dtype=int)
        self.next_car_id = 1
        self.car_id_map = {}
        self.load_initial_data()
        self.update_board_matrix()

    def load_initial_data(self):
        candidate_cars = [
            Car("red", 12, Direction.UP, 6, 8),
            Car("green", 8, Direction.LEFT, 4, 6),
            Car("orange", 4, Direction.LEFT, 1, 1),
            Car("pink", 4, Direction.DOWN, 9, 9),
            Car("blue", 6, Direction.RIGHT, 0, 7),
            Car("blue", 12, Direction.DOWN, 6, 4),
            Car("pink", 12, Direction.RIGHT, 7, 0),
            Car("yellow", 12, Direction.DOWN, 2, 2),
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
        # Obtener las celdas actuales del auto
        car_cells = set(self.get_car_cells(car))

        # Determinar las celdas que necesitan estar libres para que el auto pueda salir
        path_cells = []

        if car.direction == Direction.UP:
            # Encontrar la celda frontal (la más cercana al borde en dirección hacia arriba)
            front_row = min(row for row, _ in car_cells)
            # Verificar todas las celdas desde la frontal hasta el borde del tablero
            for r in range(front_row - 1, -1, -1):
                path_cells.append((r, car.col))

        elif car.direction == Direction.DOWN:
            # Encontrar la celda frontal (la más cercana al borde en dirección hacia abajo)
            front_row = max(row for row, _ in car_cells)
            # Verificar todas las celdas desde la frontal hasta el borde del tablero
            for r in range(front_row + 1, self.rows):
                path_cells.append((r, car.col))

        elif car.direction == Direction.LEFT:
            # Encontrar la celda frontal (la más cercana al borde en dirección hacia la izquierda)
            front_col = min(col for _, col in car_cells)
            # Verificar todas las celdas desde la frontal hasta el borde del tablero
            for c in range(front_col - 1, -1, -1):
                path_cells.append((car.row, c))

        elif car.direction == Direction.RIGHT:
            # Encontrar la celda frontal (la más cercana al borde en dirección hacia la derecha)
            front_col = max(col for _, col in car_cells)
            # Verificar todas las celdas desde la frontal hasta el borde del tablero
            for c in range(front_col + 1, self.cols):
                path_cells.append((car.row, c))

        # Verificar si hay algún obstáculo en el camino
        for r, c in path_cells:
            if 0 <= r < self.rows and 0 <= c < self.cols and self.board_matrix[r, c] != 0:
                return False

        return True

    def try_move_car(self, car):
        if len(self.platforms) >= self.max_platforms:
            return "lose"
        if self.is_path_clear(car):
            if car in self.cars:
                self.cars.remove(car)
                self.platforms.append(car)
                self.update_board_matrix()
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
