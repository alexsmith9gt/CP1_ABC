from robots import *
import matplotlib.pyplot as plt
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

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #robots currently occupying the cell
        self.occupants = []
        #list of robots that have a goal in this cell
        self.targets = []
        #robots that are staged to move to this cell in the next timestep
        self.staged_move = []
    