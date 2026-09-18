from robots import *
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
class Grid:
    def __init__(self, size:int):
        self.max_eval_step = 0
        self.current_step = 0
        self.n = size
        # matrix representing the 2-D grid
        self.matrix = []
        # filling matrix with a Cell object in each index
        for i in range(size):
            self.matrix.append([])
            for j in range(size):
                self.matrix[i].append(Cell(i,j))
        # Initialze robots
        self.robots: list[Robot] = []
        # TODO

    def visualize(self):
        # Creating the initial grid plot
        fig, ax = plt.subplots()

        # framing the grid
        ax.set_xlim(-0.5,(self.n  +0.5))
        ax.set_ylim(-0.5,(self.n + 0.5))

        # Tick Marks and grid lines
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.xaxis.set_minor_locator(MultipleLocator(0.5))
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_minor_locator(MultipleLocator(0.5))
        ax.grid(which="minor")
        ax.set_title(f"Robot Grid Navigation - {self.n}x{self.n} - t = {self.current_step}")
        plt.show()
        pass

    def step_forward(self):
        self.current_step += 1
        if self.current_step > self.max_eval_step:
            # Step the simulation, doing greedy movement
            # append to robot.position
            # TODO
            pass

    def step_backward(self):
        if self.current_step > 0:
            self.current_step -= 1
    def add_robot(self, rob):
        if type(rob) == Robot:
            self.robots.append(rob)
    

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #robots currently occupying the cell
        self.occupants = []
        #list of robots that have a goal in this cell
        self.goals = []
        #robots that are staged to move to this cell in the next timestep
        self.staged_move = []
g = Grid(5)
g.visualize()