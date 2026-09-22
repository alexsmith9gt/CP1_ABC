import numpy as np

class Robot:
    def __init__(self, initial_position, goal_position):
        self.positions = np.array([initial_position])
        self.goal = goal_position

    def can_coexist(self, other):
        pass

    def at_goal(self, current_step):
        if np.all(self.positions[current_step] == self.goal):
            return True
        return False

            
    def get_desired_new_position(self):
        delta = self.goal - self.positions[-1]
        moves = []
        if delta[0] != 0:
            moves.append(np.array([np.sign(delta[0]), 0]))
        elif delta[1] != 0:
            moves.append(np.array([0, np.sign(delta[1])]))

        new_positions = moves
        for i in range(len(new_positions)):
            new_positions[i] = new_positions[i] + self.positions[-1]

        return new_positions
    
    def move_to(self, position):
        self.positions = np.append(self.positions, [position], 0)

class Drone(Robot):
    def __init__(self, initial_position, goal_position):
        super().__init__(initial_position, goal_position)

    def can_coexist(self, other):
        if isinstance(other, Humanoid) or isinstance(other, DiffDrive):
            return True
        return False

class Humanoid(Robot):
    def __init__(self, initial_position, goal_position):
        super().__init__(initial_position, goal_position)

    def can_coexist(self, other):
        if isinstance(other, Drone):
            return True
        return False
    
class DiffDrive(Robot):
    def __init__(self, initial_position, goal_position):
        super().__init__(initial_position, goal_position)

    def can_coexist(self, other):
        if isinstance(other, Drone):
            return True
        return False