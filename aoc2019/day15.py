from helpers import *
from helpers.intcode import IntcodeComputer
import readchar
import os
from functools import cmp_to_key


def neighbor4(p):
    x, y = p[0], p[1]
    # up left right down
    return ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1))


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def GetAllAdjacentPositions(grid, target):
    adjacents = []
    for k, v in grid.items():
        if v["unit"] == target:
            for test_p in neighbor4(k):
                if grid[test_p]["unit"] == ".":
                    adjacents += [test_p]
    return adjacents


def position_clear(world, position):
    if position in world and world[position] in ".O":
        return True
    return False


def a_star(s, e, world):
    """
	s = start
	e = end
	world must support "position_clear(p) -> bool"
	todo: add different hueristics, we'll just striaght up use manahttan distnace
	"""
    closed_set = set()
    open_set = set([s])
    came_from = dict()
    g_score = {s: 0}
    f_score = {s: manhattan_distance(s, e)}

    while len(open_set) > 0:

        current = min(open_set, key=lambda o: f_score[o] if o in f_score else math.inf)

        if current == e:
            final_path = [current]
            while current in came_from:
                current = came_from[current]
                final_path += [current]
            return list(reversed(final_path))

        open_set.remove(current)
        closed_set.add(current)
        for neighbor in [
            x for x in neighbor4(current) if position_clear(world, x) or x == e
        ]:

            if neighbor in closed_set:
                continue

            if neighbor not in open_set:
                open_set.add(neighbor)

            # cost tries to make it prefer teh following movements UP, LEFT, RIGHT, DOWN in that order
            # don't need it, we can just search the spots for better options
            tentative_g_score = (
                g_score[current] + 1
            )  # reading_order_path_cost(current,neighbor)

            if neighbor in g_score and g_score[neighbor] <= tentative_g_score:
                continue  # already know better...

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + manhattan_distance(neighbor, e)
    return None


def sort_position(position1, position2):
    if position1[1] != position2[1]:
        return (position1[1] > position2[1]) - (position1[1] < position2[1])
    return (position1[0] > position2[0]) - (position1[0] < position2[0])


def print_grid(grid, robot_position, clear=False):
    x_s = [p[0] for p in grid.keys()]
    y_s = [p[1] for p in grid.keys()]

    if clear:
        _ = os.system("clear")
    for y in range(min(y_s) - 10, max(y_s) + 10):
        for x in range(min(x_s) - 10, max(x_s) + 10):
            if (x, y) == robot_position:
                print("@", end="")
            else:
                print(grid.get((x, y), " "), end="")
        print()


def problem1(problem_input):
    problem_input = [int(x) for x in problem_input.split(",")]
    cpu = IntcodeComputer(problem_input)

    cpu.run()

    grid = dict()
    robot_position = 0, 0
    grid[robot_position] = "."

    unknown_positions = list(neighbor4(robot_position))

    found_o2 = False
    while len(unknown_positions) > 0:
        # get neighbors, add all unexplored to queue
        # get closest list item
        # move to there

        reverse_grid_move = {(0, -1): 1, (-1, 0): 4, (0, 1): 2, (1, 0): 3}

        reverse_grid_move_name = {
            (0, -1): "NORTH",
            (-1, 0): "WEST",
            (0, 1): "SOUTH",
            (1, 0): "EAST",
        }

        target = unknown_positions.pop(0)
        if target in grid:
            continue

        path = a_star(robot_position, target, grid)

        step = path[1][0] - robot_position[0], path[1][1] - robot_position[1]

        if path[1] != target:
            unknown_positions.insert(0, target)

        cpu.input_queue += [reverse_grid_move[step]]
        cpu.run()

        result = cpu.output_queue.pop()

        potential_robot_space = robot_position[0] + step[0], robot_position[1] + step[1]

        if result == 0:
            grid[potential_robot_space] = "#"
        elif result == 1:
            grid[potential_robot_space] = "."
            robot_position = potential_robot_space
        elif result == 2:
            grid[potential_robot_space] = "O"
            robot_position = potential_robot_space
            o2_position = robot_position

        for p in neighbor4(robot_position):
            if p not in grid:
                unknown_positions += [p]

        # print_grid(grid,robot_position, True)

        unknown_positions.sort(key=cmp_to_key(sort_position))

    return len(a_star((0, 0), o2_position, grid)) - 1


def problem2(problem_input):
    problem_input = [int(x) for x in problem_input.split(",")]
    cpu = IntcodeComputer(problem_input)

    cpu.run()

    grid = dict()
    robot_position = 0, 0
    grid[robot_position] = "."

    unknown_positions = list(neighbor4(robot_position))

    found_o2 = False
    while len(unknown_positions) > 0:
        # get neighbors, add all unexplored to queue
        # get closest list item
        # move to there

        reverse_grid_move = {(0, -1): 1, (-1, 0): 4, (0, 1): 2, (1, 0): 3}

        reverse_grid_move_name = {
            (0, -1): "NORTH",
            (-1, 0): "WEST",
            (0, 1): "SOUTH",
            (1, 0): "EAST",
        }

        target = unknown_positions.pop(0)
        if target in grid:
            continue

        path = a_star(robot_position, target, grid)

        step = path[1][0] - robot_position[0], path[1][1] - robot_position[1]

        if path[1] != target:
            unknown_positions.insert(0, target)

        cpu.input_queue += [reverse_grid_move[step]]
        cpu.run()

        result = cpu.output_queue.pop()

        potential_robot_space = robot_position[0] + step[0], robot_position[1] + step[1]

        if result == 0:
            grid[potential_robot_space] = "#"
        elif result == 1:
            grid[potential_robot_space] = "."
            robot_position = potential_robot_space
        elif result == 2:
            grid[potential_robot_space] = "O"
            robot_position = potential_robot_space
            o2_position = robot_position

        for p in neighbor4(robot_position):
            if p not in grid:
                unknown_positions += [p]

        unknown_positions.sort(key=cmp_to_key(sort_position))

    # grid is populated
    minutes = 0
    while len([k for k, v in grid.items() if v == "."]):
        minutes += 1
        new_grid = grid.copy()
        for k, v in grid.items():
            if v == "O":
                expansion = neighbor4(k)
                for e in expansion:
                    if new_grid.get(e, " ") == ".":
                        new_grid[e] = "O"
        grid = new_grid.copy()

    return minutes
