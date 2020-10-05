from helpers import *

KEYS = "abcdefghijklmnopqrstuvwxyz"
DOORS = KEYS.upper()


def unlock_door_for_key(grid, key):
    for k, v in grid.items():
        if v == upper(key):
            v = "."


def problem1(problem_input):
    grid = dict()
    doors = []
    keys = []
    for y, line in enumerate(problem_input):
        for x, char in enumerate(line):
            grid[(x, y)] = char
            if char in KEYS:
                keys += [char]
            if char in DOORS:
                doors += [char]

    max_y = y
    max_x = x

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(grid[(x, y)], end="")
        print()

    keys.sort()
    doors.sort()
    print("Keys:", keys)
    print("Doors:", doors)
    return 0


def problem2(problem_input):
    return None
