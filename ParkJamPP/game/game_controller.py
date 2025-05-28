from game.car import Car, Direction
from game.platform import PlatformManager
from game.passenger import PassengerQueue
import numpy as np #Used for efficient operations on the board matrix


class GameController:
    def __init__(self):
        self.cars = []
        self.original_cars = []  # saves original position for reset button
        #matrix size
        self.rows = 10
        self.cols = 10
        self.board_matrix = np.zeros((self.rows, self.cols), dtype=int) #2D numpy matrix to track which car ID is in which cell
        self.next_car_id = 1 #Counter for assigning IDs
        self.car_id_map = {} #Maps car ID to object
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

        #Custom passenger queue
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

    #Loads car initial data and positions in the board
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

        #Checks every car on the list, maps them in the matrix and makes sure none
        #are getting outside the board, if they are, an error message pops up
        for car in candidate_cars:
            for r, c in self.get_car_cells_static(car):
                if not (0 <= r < self.rows and 0 <= c < self.cols):
                    raise ValueError(
                        f"Auto {car.color} sobresale del tablero en dirección {car.direction} desde ({car.row}, {car.col})")
            #Saves car in ID map, assigns ID and increments ID number for next car
            self.car_id_map[self.next_car_id] = car
            car.id = self.next_car_id
            self.next_car_id += 1
            #Adds to car list and clones to original cars list
            self.cars.append(car)
            self.original_cars = [Car(car.color, car.capacity, car.direction, car.row, car.col)
                                  for car in candidate_cars]
            for c1, c2 in zip(self.original_cars, candidate_cars):
                c1.id = c2.id  # maintains ID consistency by assigning same ID to the original car and the active car

        self.update_board_matrix() #Rebuilds the board placing cars in their appropiate cells

    #Class for the correct updatig of the board to ensure collisions and cars exiting board
    def update_board_matrix(self):
        self.board_matrix = np.zeros((self.rows, self.cols), dtype=int) #Reseats the board to zeroes and ensures correct data is processed
        #Iterates all cars currently on the board and marks cells with the car ID to
        # ensure collisions and correct depiction of where the car is located
        for car in self.cars:
            cells = self.get_car_cells(car)
            for row, col in cells:
                if 0 <= row < self.rows and 0 <= col < self.cols:
                    self.board_matrix[row, col] = car.id

    def get_car_cells(self, car):
        return self.get_car_cells_static(car)

    #Creates an empty list for the coordinates of the cars depending on their position
    @staticmethod
    def get_car_cells_static(car):
        """Cells that rhe car uses from head to back"""
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

    #Determines if the car has a clear path in front of it, all the
    # way to the edge of the board by storing all the cells the car currently occupies, then
    # finds the front-most row or column to build path_cells that check each space ahead of the nose of the car
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

    # Tries to move a car off the board and into the platform zone. It checks
    def try_move_car(self, car):

        #For lose popup window when platforms are full
        if self.platform_manager.is_full():
            return "lose"

        #Checks that the path is clear and if the car is still currently in the board
        # then removes the car from the list of active (on board) cars
        if self.is_path_clear(car):
            if car in self.cars:
                self.cars.remove(car)
                self.update_board_matrix() #Updates matrix without the cars
                self.platform_manager.add_car_to_platform(car) #Sends car to boarding platform

                # Instantly boards any waiting passenger if color matches
                self.platform_manager.board_waiting_passengers()

                return "moved"

        return "blocked"


    # Tells which car is at what position or occupying which cell on the board
    def get_car_at_position(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            car_id = self.board_matrix[row, col]
            if car_id > 0:
                return self.car_id_map.get(car_id)
        return None

    #Debugging method to find if the cars are appearing correctly in the matrix
    #gets thats currently on the board and prints it on the console with cars and their direction
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
        # Clones original cars
        self.cars = [Car(c.color, c.capacity, c.direction, c.original_row, c.original_col)
                     for c in self.original_cars]
        for c1, c2 in zip(self.cars, self.original_cars):
            c1.id = c2.id
            c1.original_row = c2.original_row
            c1.original_col = c2.original_col

        # Restores map and ID
        self.car_id_map = {car.id: car for car in self.cars}
        self.update_board_matrix()

        # Resests platforms and all passengers
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

