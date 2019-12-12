from helpers.all_of_them import *
from collections import defaultdict

DIRS = UP, RIGHT, DOWN, LEFT = (0, -1), (1, 0), (0, 1), (-1, 0)

LEFT_TURN = {UP: LEFT, LEFT: DOWN, DOWN: RIGHT, RIGHT: UP}

RIGHT_TURN = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}

TURNS = [LEFT_TURN, RIGHT_TURN]

DIR_PRINT = {UP: "^", DOWN: "v", LEFT: "<", RIGHT: ">"}


def problem1(problem_input):
    cpu = Computer([int(x) for x in problem_input.split(",")])

    robot_location = (0, 0)
    grid = defaultdict(lambda: 0)
    robot_facing = UP
    cpu.run()
    while not cpu.halted:
        if cpu.awaiting_input:
            cpu.input_queue += [grid[robot_location]]

            cpu.run()

        if len(cpu.output_queue) > 0:

            paint = cpu.output_queue.pop(0)
            turn_type = cpu.output_queue.pop(0)
            grid[robot_location] = paint
            robot_facing = TURNS[turn_type][robot_facing]
            robot_location = (
                robot_location[0] + robot_facing[0],
                robot_location[1] + robot_facing[1],
            )

    return len(grid.keys())


def problem2(problem_input):
    cpu = Computer([int(x) for x in problem_input.split(",")])
    robot_location = (0, 0)
    grid = defaultdict(lambda: 0)
    grid[robot_location] = 1
    robot_facing = UP
    cpu.run()
    while not cpu.halted:
        if cpu.awaiting_input:
            cpu.input_queue += [grid[robot_location]]

            cpu.run()

        if len(cpu.output_queue) > 0:

            paint = cpu.output_queue.pop(0)
            turn_type = cpu.output_queue.pop(0)
            grid[robot_location] = paint
            robot_facing = TURNS[turn_type][robot_facing]
            robot_location = (
                robot_location[0] + robot_facing[0],
                robot_location[1] + robot_facing[1],
            )

    x_vals = [k[0] for k in grid.keys()]
    y_vals = [k[1] for k in grid.keys()]
    min_x = min(x_vals)
    max_x = max(x_vals)
    min_y = min(y_vals)
    max_y = max(y_vals)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if grid[(x, y)] == 1:
                print("#", end="")
            else:
                print(" ", end="")
        print()

    return "ABOVE"
