import numpy as np

class Robot:
    def __init__(self, initial_position, goal_position):
        self.positions = np.array([initial_position])
        self.goal = goal_position

    def can_coexist(self, other):
        pass

    def get_desired_moves(self):
        pass


class Drone(Robot):
    def __init__(self, initial_position, goal_position):
        super.__init__(self, initial_position, goal_position)

    def can_coexist(self, other):
        if isinstance(other, Humanoid) or isinstance(other, DiffDrive):
            return True
        return False

class Humanoid(Robot):
    def __init__(self, initial_position, goal_position):
        super.__init__(self, initial_position, goal_position)

    def can_coexist(self, other):
        if isinstance(other, Drone):
            return True
        return False
    
class DiffDrive(Robot):
    def __init__(self, initial_position, goal_position):
        super.__init__(self, initial_position, goal_position)

    def can_coexist(self, other):
        if isinstance(other, Drone):
            return True
        return False