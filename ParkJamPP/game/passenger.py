from collections import deque #For fast appending and popping in the list

# Represents a passenger in the line to board a car
class Passenger:

    # Initializes the passenger with the given color
    def __init__(self, color: str):
        self.color = color

#Manages the line of passengers waiting to board cars in the game
class PassengerQueue:
    def __init__(self, car_list):
        self.queue = deque()

    # Removes and returns the passenger at the front of the queue.
    def next_passenger(self):
        if self.queue:
            return self.queue.popleft()
        return None

    #Returns next passenger in line without removing them
    def peek(self):
        if self.queue:
            return self.queue[0]
        return None

    #Method to add a custom queue with sintax: 'red','yellow', 'orange'...
    def insert_custom_queue(self, color_sequence):
        self.queue = deque(Passenger(color) for color in color_sequence)

    #Method to know if the queue list is empty
    def is_empty(self):
        return not self.queue

    #Displays number of passengers left in queue
    def __len__(self):
        return len(self.queue)
