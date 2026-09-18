from robots import *

class Grid:
    def __init__(self, size:int):
        self.max_eval_step = 0
        self.current_step = 0

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