
#Administer thr car´s platforms where the vehicles freed from the board wait for passengers to board them
class PlatformManager:

    def __init__(self, max_platforms=6):
        self.platforms = []  #Creates an empy list for the cars that will be on the platforms
        self.max_platforms = max_platforms #Defines the max number of platforms available
        self.passenger_queue = None

    def set_passenger_queue(self, queue):
        self.passenger_queue = queue #Allows methods to access to the queue to allow passenger boarding

    def add_car_to_platform(self, car):
        """
        Adds car to the platform. Boards passengers immediately if available.
        If the car capacity is full, deletes de car.
        """
        if len(self.platforms) >= self.max_platforms:
            return False

        car.boarded = 0
        while car.boarded < car.capacity and not self.passenger_queue.is_empty():
            if self.passenger_queue.peek().color == car.color:
                self.passenger_queue.next_passenger()
                car.boarded += 1
            else:
                break

        if car.boarded < car.capacity:
            self.platforms.append(car)
            print(f"Auto {car.color} parcialmente abordado ({car.boarded}/{car.capacity})")
        else:
            print(f"Auto {car.color} completamente abordado al entrar y eliminado ({car.capacity} pasajeros)")

        return True

    def board_waiting_passengers(self):
        """
        Tries to board all possible passengers when they are in front of the line
        to cars of their color in the platforms.
        Code repeats until no matchings occur.
        """
        if self.passenger_queue.is_empty():
            return

        # Using a controlled loop to not modify this list while going through it
        while True:
            if self.passenger_queue.is_empty():
                break

            next_color = self.passenger_queue.peek().color
            matched = False

            for car in self.platforms:
                if car.color == next_color and car.boarded < car.capacity:
                    self.passenger_queue.next_passenger()
                    car.boarded += 1
                    print(f"Pasajero {next_color} abordó auto en plataforma ({car.boarded}/{car.capacity})")

                    if car.boarded == car.capacity:
                        print(f"Auto {car.color} completado en plataforma. Será eliminado.")
                        self.platforms.remove(car)

                    matched = True
                    break  # Processing one passenger each cicle

            if not matched:
                break  # Exiting when no one is available to board

    def get_platform_cars(self):
        return self.platforms #Returns cars not completely boarded

    def is_full(self):
        return len(self.platforms) >= self.max_platforms #Returns true as long as all platforms are full
