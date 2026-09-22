from grid import Grid

if __name__ == "__main__":
    grid = Grid(5)
    for _ in range(100):
        grid.step_forward()