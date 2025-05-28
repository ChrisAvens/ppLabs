# ParkJamPP

**ParkJamPP** is a Python + PyQt6 game inspired by the classic [Car Park Jam] puzzle, where you must move cars off a congested board and load passengers according to color and capacity. Your objective is to manage traffic, avoid blocking, and fill all cars with their matching passengers before space runs out.

---

## How to Play

1. **Click on a car** to try moving it.
2. The car can only exit if its path is **clear**.
3. Once it leaves the board, it enters the **platform** and begins **boarding passengers** of its color.
4. If a car fills completely, it leaves with a cheerful animation and sound.
5. The game ends successfully when all passengers are boarded — or **fails** if there's no more room on the platform.

---

## Game Mechanics

- The **board** is a 10×10 grid.
- Each car has a:
  - **Color** (e.g., red, green, blue),
  - **Capacity** (number of passengers),
  - **Direction** (up/down/left/right),
  - **Visual size**, proportional to its capacity.
- **Passengers** are queued and must board cars that match their color.
- **Platforms** can hold a maximum of 6 cars at once.
- Real-time **animations** and **sound effects** enhance gameplay feedback.

---

## Project Structure

ParkJamPP/
├── main.py # Entry point
├── assets/ # Images and sounds
│ ├── window_background.png
│ ├── board_background.png
│ ├── cars/ # Car images (color + capacity) and board variants
│ └── sounds/ # Sound effects
├── game/
│ ├── car.py # Car and direction logic
│ ├── game_controller.py # Game logic, board control
│ ├── passenger.py # Passenger queue logic
│ └── platform.py # Platform and boarding handling
└── ui/
└── game_window.py # PyQt6 UI, animations, interactions


---

## Getting Started

### Requirements

Make sure you have **Python 3.10+** and **PyQt6** installed:

PyQt6
numpy


## Run the game

TO run the game simply execute:

main.py

## Assets

Car images are stored by color and capacity in assets/cars/.

Passengers are shown using icons or emoji if images are missing.

Backgrounds and platform-specific car images enhance immersion.

Sounds include:

car_move.wav (successful exit),

error.wav (blocked move),

boarding.wav,

leave_platform.wav.

## Built With

Python 3

PyQt6 — for GUI and animation

NumPy — for board matrix logic

## Author
Developed by **Christian Isaac Avendaño Tellez** as a project for the programming paradigms class in the Universidade Autonoma de Lisboa.