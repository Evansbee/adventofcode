from helpers import *
from collections import defaultdict

DIRS = DIRECTIONS = UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
COMMANDS = {"U": 0, "D": 1, "L": 2, "R": 3}


def printgrid(grid):
    x_vals = [x for x, _ in grid.keys()]
    y_vals = [y for _, y in grid.keys()]

    for y in range(min(y_vals) - 1, max(y_vals) + 2):
        for x in range(min(x_vals) - 1, max(x_vals) + 2):
            if x == 0 and y == 0:
                print("*", end="")
            elif len(grid[(x, y)]["lines"]) == 0:
                print(".", end="")
            elif len(grid[(x, y)]["lines"]) == 1:
                print(grid[(x, y)]["lines"][0], end="")
            else:
                print("X", end="")
        print()


def problem1(problem_input):
    grid = defaultdict(lambda: defaultdict(list))
    for i, line in enumerate(problem_input):
        commandlist = line.split(",")
        cursor = (0, 0)
        distance = 0
        for command in commandlist:
            direction = DIRS[COMMANDS[command[0]]]
            count = int(command[1:])
            for _ in range(count):
                distance += 1
                cursor = (cursor[0] + direction[0], cursor[1] + direction[1])
                if i not in grid[cursor]["lines"]:
                    grid[cursor]["lines"] += [i]
                    grid[cursor]["distances"] += [distance]

    collision_locations = [k for k, v in grid.items() if len(v["lines"]) > 1]
    collission_distances = [abs(v[0]) + abs(v[1]) for v in collision_locations]

    distances_traveled = [
        sum(v["distances"]) for k, v in grid.items() if k in collision_locations
    ]

    return min(collission_distances)


def problem2(problem_input):
    grid = defaultdict(lambda: defaultdict(list))
    for i, line in enumerate(problem_input):
        commandlist = line.split(",")
        cursor = (0, 0)
        distance = 0
        for command in commandlist:
            direction = DIRS[COMMANDS[command[0]]]
            count = int(command[1:])
            for _ in range(count):
                distance += 1
                cursor = (cursor[0] + direction[0], cursor[1] + direction[1])
                if i not in grid[cursor]["lines"]:
                    grid[cursor]["lines"] += [i]
                    grid[cursor]["distances"] += [distance]

    collision_locations = [k for k, v in grid.items() if len(v["lines"]) > 1]

    distances_traveled = [
        sum(v["distances"]) for k, v in grid.items() if k in collision_locations
    ]

    return min(distances_traveled)
