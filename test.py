from grid import Grid
import numpy as np

if __name__ == "__main__":
    for i in range(10000):
        grid = Grid(5)
        while grid.step_forward():
            pass

    print("Test finished successfuly")