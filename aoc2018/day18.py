from helpers import *
from collections import defaultdict


def get_neighbors(grid, p):
    positions = set()
    for x in [p[0] - 1, p[0], p[0] + 1]:
        for y in [p[1] - 1, p[1], p[1] + 1]:
            positions.add((x, y))

    positions.remove(p)

    return [grid[l] for l in positions if l in grid]


def do_step(input_grid):
    output_grid = defaultdict(lambda: ".")
    for k, v in input_grid.items():
        neighbors = get_neighbors(input_grid, k)
        output_grid[k] = v

        if v == "." and neighbors.count("|") >= 3:
            output_grid[k] = "|"

        if v == "|" and neighbors.count("#") >= 3:
            output_grid[k] = "#"

        if v == "#":
            if neighbors.count("#") >= 1 and neighbors.count("|") >= 1:
                output_grid[k] = "#"
            else:
                output_grid[k] = "."
    return output_grid


def problem1(problem_input):
    grid = defaultdict(lambda: ".")
    for y, line in enumerate(problem_input):
        for x, t in enumerate(line):
            grid[(x, y)] = t
    for _ in range(10):
        grid = do_step(grid)

    return list(grid.values()).count("|") * list(grid.values()).count("#")


def problem2(problem_input):
    history = []
    grid = defaultdict(lambda: ".")
    for y, line in enumerate(problem_input):
        for x, t in enumerate(line):
            grid[(x, y)] = t

    history.append(grid.copy())
    for c in range(1000000000):
        print(c, end=" ")
        grid = do_step(grid)
        if grid not in history:
            history.append(grid.copy())
        else:
            print("FOUND LOOP at ", history.index(grid))
            idx = 1000000000 - history.index(grid)
            history = history[history.index(grid) :]
            idx = idx % len(history)
            print(history)
            grid = history[idx]
            return list(grid.values()).count("|") * list(grid.values()).count("#")
    return list(grid.values()).count("|") * list(grid.values()).count("#")
