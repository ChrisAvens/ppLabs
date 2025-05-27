import random
from collections import deque

class Passenger:
    def __init__(self, color: str):
        self.color = color

    def __repr__(self):
        return f"👤{self.color}"

class PassengerQueue:
    def __init__(self, car_list):
        self.queue = deque()
        self.generate_passengers_from_cars(car_list)

    def generate_passengers_from_cars(self, cars):
        passengers = []
        color_count = {}
        for car in cars:
            color_count.setdefault(car.color, 0)
            color_count[car.color] += car.capacity

        for color, total in color_count.items():
            passengers.extend(Passenger(color) for _ in range(total))

        random.shuffle(passengers)
        self.queue = deque(passengers)
