from robots import *
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import numpy as np

class Grid:
    def __init__(self, size:int=5):
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

        # Positional data lists for graphing:
        self.drones_x = []
        self.drones_y = []
        self.drones_goals_x = []
        self.drones_goals_y =[]

        self.humans_x = []
        self.humans_y = []
        self.humans_goals_x = []
        self.humans_goals_y = []

        self.drives_x = []
        self.drives_y = []
        self.drives_goals_x = []
        self.drives_goals_y = []
        self.num_robots = 2*size
        robot_types = np.random.choice([Drone, Humanoid, DiffDrive], self.num_robots)
        for i in range(self.num_robots):
            goal_pos = np.random.random_integers(0, size-1, (size,size))
            init_pos = np.random.random_integers(0, size-1, (size,size))

            # Make sure we initialize each robot in a valid location
            while True:
                new_robot = robot_types[i](init_pos, goal_pos)
                for j in len(self.robots):
                    if self.robots[j].positions[0] == init_pos and not self.robots[j].can_coexist(new_robot):
                        init_pos = np.random.random_integers(0, size-1, (size,size))
                        continue
                self.robots[i] = new_robot
                break

        
           

    def visualize(self):
        #collect positional data

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
            # Step the simulation, doing greedy movement with conflict resolution            
            conflict_resolution_positions = {}
            robots_to_move = [i for i in range(self.num_robots)]
            for i in range(self.num_robots):
                robot = self.robots[i]
                # Nothing to do if already at the goal
                if robot.positions[-1] == robot.goal:
                    robot.positions = np.append(robot.positions, robot.goal, 0)
                    robot.move_to(robot.goal)
                    robots_to_move.remove(i)
                else:
                    new_pos = robot.get_desired_new_position()

                    # Robots are always allowed to move to their goal state
                    if new_pos[0] == robot.goal:
                        robot.move_to(robot.goal)
                        robots_to_move.remove(i)
                    else:
                        displacement = robot.positions[-1] - robot.goal
                        dist = np.sum(np.abs(displacement))
                        for pos in new_pos:
                            d = {'robot_id': i, 'dist_to_goal': dist}
                            if pos in conflict_resolution_positions:
                                conflict_resolution_positions[pos] += [d]
                            else:
                                conflict_resolution_positions[pos] = [d]

            # Iterate over proposed movement locations and select the robot
            # with greatest distance to the goal
            for pos, data in conflict_resolution_positions.items():
                max_dist = 0
                max_dist_robot = -1
                for item in data:
                    if item['robot_id'] in robots_to_move and item['dist_to_goal'] > max_dist:
                        max_dist = item['dist_to_goal']
                        max_dist_robot = item['robot_id']

                if max_dist_robot != -1:
                    robot.move_to(pos)
                    robots_to_move.remove(max_dist_robot)

            # If we were unable to move a robot, make it stay still and wait
            for id in robots_to_move:
                self.robots[id].move_to(self.robots[id].positions[-1])


    def step_backward(self):
        if self.current_step > 0:
            self.current_step -= 1
    def add_robot(self, rob):
        if type(rob) == Robot:
            self.robots.append(rob)
    def get_positional_data(self):
        for robot in self.robots():
            if robot.at_goal(self.current_step):
                continue
            else:
                if type(robot) == Drone

    

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