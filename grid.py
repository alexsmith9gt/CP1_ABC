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
                    if ((np.all(self.robots[j].positions[0] == init_pos) and not self.robots[j].can_coexist(new_robot))
                        or np.all(init_pos == goal_pos)):
                        init_pos = np.random.random_integers(0, size-1, (2,))
                        break
                else: #only runs if for loop terminates naturally (not by break)
                    self.robots.append(new_robot)
                    break

        self.collision_check()




    def visualize(self, return_on_end=False):
        fig, ax = plt.subplots()

        def update_plot():
            ax.clear()

            ax.set_autoscale_on(False)

            for robot in self.robots:
                robo_pos = robot.positions[self.current_step]
                goal_pos = robot.goal
                if (robo_pos == goal_pos).all():
                    continue

                # Offset each robot and goal so overlapping entries remain visible.
                rng = np.random.default_rng()
                rand_vals = (rng.random(2) * .6) - .3
                robo_pos = robo_pos.astype(float) + rand_vals
                goal_pos = goal_pos.astype(float) + rand_vals
                if type(robot) == Drone:
                    color = 'red'
                    shape = 's'
                elif type(robot) == Humanoid:
                    color = 'blue'
                    shape = 'o'
                elif type(robot) == DiffDrive:
                    color = 'green'
                    shape = '^'

                ax.scatter(robo_pos[0], robo_pos[1], c = color, marker = shape)
                ax.scatter(goal_pos[0], goal_pos[1], c = color, marker = "d")
                ax.plot([robo_pos[0],goal_pos[0]],
                        [robo_pos[1],goal_pos[1]],
                        color = color, linestyle = '--' )

            # Empty scatterplots provide the legend entries.
            ax.scatter([],[], color = 'red', marker = 's', label = "Drone")
            ax.scatter([],[], color = 'blue', marker = 'o', label = "Humanoid")
            ax.scatter([],[], color = 'green', marker = '^', label = "Diff Drive")
            ax.scatter([],[], color = 'black', marker = 'd', label = "Goal")

            ax.xaxis.set_major_locator(MultipleLocator(1))
            ax.xaxis.set_minor_locator(MultipleLocator(0.5))
            ax.yaxis.set_major_locator(MultipleLocator(1))
            ax.yaxis.set_minor_locator(MultipleLocator(0.5))
            ax.grid(which="minor")
            ax.legend()
            ax.set_title(f"Robot Grid Navigation - {self.n}x{self.n} - t = {self.current_step}")

            ax.set_xlim(-0.5,(self.n - 0.5))
            ax.set_ylim(-0.5,(self.n - 0.5))
            ax.set_aspect('equal', adjustable='box')
            fig.canvas.draw_idle()

        def on_key(event):
            if event.key == 'left' and self.current_step > 0:
                self.step_backward()
                update_plot()
            elif event.key == 'right':
                running = self.step_forward()
                update_plot()
                if not running:
                    return

        fig.canvas.mpl_connect('key_press_event', on_key)
        update_plot()
        plt.show()

    def step_forward(self):
        if self.current_step == self.max_eval_step and self.simulation_finished():
            return False

        total_moves = 0
        self.current_step += 1
        if self.current_step > self.max_eval_step:
            self.max_eval_step = self.current_step
            # Step the simulation, doing greedy movement with conflict resolution            
            conflict_resolution_positions = {}
            desired_moves_per_robot = {}
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
                    desired_moves_per_robot[i] = new_pos
                    # Robots are always allowed to move to their goal state
                    if np.all(new_pos[0] == robot.goal):
                        robot.move_to(robot.goal)
                        robots_to_move.remove(i)
                        total_moves += 1
                    else:
                        displacement = robot.positions[-1] - robot.goal
                        dist = np.sum(np.abs(displacement))
                        for pos in new_pos:
                            d = {'robot_id': i, 'dist_to_goal': dist}
                            if tuple(pos) in conflict_resolution_positions:
                                conflict_resolution_positions[tuple(pos)] += [d]
                            else:
                                conflict_resolution_positions[tuple(pos)] = [d]

            
            moves_this_iter = 1
            while moves_this_iter:
                moves_this_iter = 0

                # Iterate over proposed movement locations and select the robot
                # with greatest distance to the goal
                for pos, data in conflict_resolution_positions.items():
                    max_dist = 0
                    max_dist_robot = -1
                    
                    for item in data:
                        if item['robot_id'] in robots_to_move and item['dist_to_goal'] > max_dist:
                            id1 = item['robot_id']
                            robot1 = self.robots[id1]

                            # Check for collisions before proposing this movement
                            collision = False
                            for id2 in range(self.num_robots):
                                robot2 = self.robots[id2]
                                if id1 != id2 and \
                                    np.all(pos == robot2.positions[-1]) and \
                                    not robot2.at_goal(-1) and \
                                    not robot1.can_coexist(robot2):
                                        collision = True
                                        break
                            if not collision:
                                max_dist = item['dist_to_goal']
                                max_dist_robot = item['robot_id']

                    # Move the best robot if one was found
                    if max_dist_robot != -1:
                        self.robots[max_dist_robot].move_to(pos)
                        robots_to_move.remove(max_dist_robot)
                        moves_this_iter += 1

                # Check if any robots can swap locations
                for id1 in robots_to_move:
                    robot1 = self.robots[id1]
                    pos1 = robot1.positions[-1]
                    for id2 in robots_to_move:
                        if id1 == id2:
                            continue
                        robot2 = self.robots[id2]
                        pos2 = robot2.positions[-1]
                        if np.any(np.all(pos1 == desired_moves_per_robot[id2], axis=1)) and \
                           np.any(np.all(pos2 == desired_moves_per_robot[id1], axis=1)):

                            # Collision checking
                            collision = False
                            for id3 in range(self.num_robots):
                                robot3 = self.robots[id3]
                                if id1 != id3 and id3 != id2 and \
                                    np.all(pos2 == robot3.positions[-1]) and \
                                    not robot3.at_goal(-1) and \
                                    not robot1.can_coexist(robot3):
                                        collision = True
                                        break
                                if id2 != id3 and id3 != id1 and \
                                    np.all(pos1 == robot3.positions[-1]) and \
                                    not robot3.at_goal(-1) and \
                                    not robot2.can_coexist(robot3):
                                        collision = True
                                        break

                            # Swap the robot locations if no collisions
                            if not collision:
                                robot1.move_to(pos2)
                                robots_to_move.remove(id1)
                                robot2.move_to(pos1)
                                robots_to_move.remove(id2)
                                moves_this_iter += 2
                total_moves += moves_this_iter
                
            if total_moves == 0:
                # This only occurs in the very very special edge case where we have a loop of robots which all want to move together in a loop 
                # This is solved naively by moving all of the robots. 
                # Warning: This will cause collisions in the very very extremely rare case when there is a robot outside the loop that wants to move into the loop
                if len(robots_to_move) == 4:
                    for id in robots_to_move:
                        self.robots[id].move_to(desired_moves_per_robot[id][0])
                    robots_to_move.clear()
                robots_in_loop = []
                for id1 in robots_to_move:
                    robot1 = self.robots[id1]
                    pos1 = robot1.positions[-1]
                    num_neighbors = 0
                    for id2 in robots_to_move:
                        robot2 = self.robots[id2]
                        pos2 = robot2.positions[-1]
                        if np.sum(np.abs(pos1 - pos2)) == 1:
                            num_neighbors += 1

                    if num_neighbors > 1:
                        robots_in_loop += [id1]

                for id in robots_in_loop:
                    self.robots[id].move_to(desired_moves_per_robot[id][0])
                    robots_to_move.remove(id)

            # If we were unable to move a robot, make it stay still and wait
            for id in robots_to_move:
                self.robots[id].move_to(self.robots[id].positions[-1])

            self.collision_check()

        return True

    def step_backward(self):
        if self.current_step > 0:
            self.current_step -= 1

    def simulation_finished(self):
        # Return true if all robots are at their goal, false otherwise
        for robot in self.robots:
            if not np.all(robot.positions[-1] == robot.goal):
                return False
        return True

    def collision_check(self):
        for i in range(self.num_robots):
            for j in range(self.num_robots):
                robot1 = self.robots[i]
                robot2 = self.robots[j]
                if i != j and \
                np.all(robot1.positions[-1] == robot2.positions[-1]) and \
                not (robot1.at_goal(-1) or robot2.at_goal(-1)) and \
                not robot1.can_coexist(robot2):
                    print(f"Collision case found at {robot1.positions[-1]}!")
