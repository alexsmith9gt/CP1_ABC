from grid import Grid
import msvcrt
import matplotlib.pyplot as plt

def menu_options():
    print("\'right arrow\': move forward by one timestep\n" \
        "\'left arrow\': move backward by one timestep\n" \
        "\'q\': terminate the program\n")


if __name__ == "__main__":
    # grid = Grid(5)
    # for _ in range(5):
    #     grid.visualize()
    #     grid.step_forward()
    # grid.visualize()
    print("Hello! Welcome to the Warehouse Robot Manager Visualizer")
    print("This is the submission for Challenge Problem 1 by Alex Smith and Ben Falco")
    print("Please enter the size of the grid you would like and hit Enter:")
    size = input()
    grid = Grid(int(size))
    print("Once you start these will be your commands:")
    menu_options()
    while True:
        print("Click \'s\' and hit enter to start")
        if input() == 's':
            break
    grid.visualize()
    
    # while True:
    #     inp = msvcrt.getch()
    #     print(inp)
    #     if b'K' in inp: #left arrow key
    #         if grid.current_step > 0:
    #             grid.step_backward()
    #             plt.close()
    #             grid.visualize()
    #     if b'M' in inp: #right arrow key
    #         grid.step_forward()
    #         plt.close()
    #         grid.visualize()
    #     if b'h' in inp: #h key
    #         menu_options()
    #     if b'\x1b' in inp: #escape key
    #         break

