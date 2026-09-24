from grid import Grid
import matplotlib.pyplot as plt

def menu_options():
    print("\'right arrow\': move forward by one timestep\n" \
        "\'left arrow\': move backward by one timestep\n" \
        "\'q\': terminate the program\n")


if __name__ == "__main__":
    print("Hello! Welcome to the Warehouse Robot Manager Visualizer")
    print("This is the submission for Challenge Problem 1 by Alex Smith and Ben Falco")
    print("Please enter the size of the grid you would like and hit Enter:")
    size = input()
    grid = Grid(int(size))
    print("Once you start these will be your commands:")
    menu_options()
    while True:
        print("Click \'s\' and hit enter to start")
        if input() == 's':
            break
    grid.visualize()
    