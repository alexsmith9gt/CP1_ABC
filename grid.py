from robots import *
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import numpy as np

class Grid:
    def __init__(self, size:int=5):
        self.max_eval_step = 0
        self.current_step = 0
        # Initialze robots
        self.robots: list[Robot] = []
        self.n = size
        self.num_robots = 2*size

        # Initialization
        robot_types = np.random.choice([Drone, Humanoid, DiffDrive], self.num_robots)
        for i in range(self.num_robots):
            goal_pos = np.random.random_integers(0, size-1, (2,))
            init_pos = np.random.random_integers(0, size-1, (2,))

            # Make sure we initialize each robot in a valid location
            while True:
                new_robot = robot_types[i](init_pos, goal_pos)
                for j in range(len(self.robots)):
                    if np.all(self.robots[j].positions[0] == init_pos) and not self.robots[j].can_coexist(new_robot):
                        init_pos = np.random.random_integers(0, size-1, (2,))
                        continue
                self.robots.append(new_robot)
                break

        
           

    def visualize(self):

        # Creating the initial grid plot
        fig, ax = plt.subplots()

        # framing the grid
        ax.set_xlim(-0.5,(self.n  +0.5))
        ax.set_ylim(-0.5,(self.n + 0.5))

        # collecting and plotting data for each robot type
        for robot in self.robots:
            robo_pos = robot.positions[self.current_step]
            goal_pos = robot.goal

            if type(robot) == Drone:
                color = 'red'
                shape = 's'
            elif type(robot) == Humanoid:
                color = 'blue'
                shape = 'o'
            elif type(robot) == DiffDrive:
                color = 'green'
                shape = '^'

            # scatter plotting robots and goals
            ax.scatter(robo_pos[0], robo_pos[1], c = color, marker = shape)
            ax.scatter(goal_pos[0], goal_pos[1], c = color, marker = "d")
            # for i in range(len(robo_type)):
            #     ax.plot([robo_pos[i][0],goal_pos[i][0]], #x values for robot and goal
            #             [robo_pos[i][1],goal_pos[i][1]], #y values for robot and goal
            #              color = color, linestyle = '--' ) 
            

        # Tick Marks and grid lines
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.xaxis.set_minor_locator(MultipleLocator(0.5))
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_minor_locator(MultipleLocator(0.5))
        ax.grid(which="minor")
        ax.set_title(f"Robot Grid Navigation - {self.n}x{self.n} - t = {self.current_step}")
        plt.show()

    def step_forward(self):
        self.current_step += 1

        if self.current_step > self.max_eval_step:
            # Step the simulation, doing greedy movement with conflict resolution            
            conflict_resolution_positions = {}
            robots_to_move = [i for i in range(self.num_robots)]
            for i in range(self.num_robots):
                robot = self.robots[i]
                # Nothing to do if already at the goal
                if np.all(robot.positions[-1] == robot.goal):
                    robot.positions = np.append(robot.positions, [robot.goal], 0)
                    robot.move_to(robot.goal)
                    robots_to_move.remove(i)
                else:
                    new_pos = robot.get_desired_new_position()

                    # Robots are always allowed to move to their goal state
                    if np.all(new_pos[0] == robot.goal):
                        robot.move_to(robot.goal)
                        robots_to_move.remove(i)
                    else:
                        displacement = robot.positions[-1] - robot.goal
                        dist = np.sum(np.abs(displacement))
                        for pos in new_pos:
                            d = {'robot_id': i, 'dist_to_goal': dist}
                            if tuple(pos) in conflict_resolution_positions:
                                conflict_resolution_positions[tuple(pos)] += [d]
                            else:
                                conflict_resolution_positions[tuple(pos)] = [d]

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
                    self.robots[max_dist_robot].move_to(pos)
                    robots_to_move.remove(max_dist_robot)

            # If we were unable to move a robot, make it stay still and wait
            for id in robots_to_move:
                self.robots[id].move_to(self.robots[id].positions[-1])


    def step_backward(self):
        if self.current_step > 0:
            self.current_step -= 1
                
