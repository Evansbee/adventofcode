from helpers import *
import math
import pdb
from colorama import init, Fore, Style


def factors(a):
    f = set(
        [1]
    )  # this is sort of incorrect, but it solves the 0 case and everyone has a 1 in their factors anyway

    for i in range(1, int(math.sqrt(abs(a))) + 1):
        if (abs(a) % i) == 0:
            f.add(i)
            f.add(abs(a) // i)
    if a < 0:
        for i in f.copy():
            f.add(-i)
    return f


def gcf(a, b):
    if a == 0 or b == 0:
        a, b = a + b, a + b
    fa = factors(a)
    fb = factors(b)
    return int(max(list(fa & fb)))


def printgrid(grid):
    x_max = max([k[0] for k in grid.keys()])
    y_max = max([k[1] for k in grid.keys()])

    for y in range(y_max + 1):
        for x in range(x_max + 1):
            if grid[(x, y)] == "*":
                print(Fore.RED + grid[(x, y)] + Fore.RESET, end="")
            elif grid[(x, y)] == "x":
                print(Fore.LIGHTBLACK_EX + grid[(x, y)] + Fore.RESET, end="")
            elif grid[(x, y)] == ".":
                print(Fore.LIGHTBLACK_EX + grid[(x, y)] + Fore.RESET, end="")
            else:
                print(grid[(x, y)], end="")
        print()
    print(f'Number of Visible Asteroids: {list(grid.values()).count("#")}\n\n')


def problem1(problem_input):
    grid = dict()

    for y, line in enumerate(problem_input):
        for x, val in enumerate(line):
            grid[(x, y)] = val

    print(f'Astroid Count: {list(grid.values()).count("#")}')
    asteroid_locations = {k: 0 for k, v in grid.items() if v == "#"}

    for base_location in asteroid_locations.keys():
        working_grid = grid.copy()
        working_grid[
            base_location
        ] = "*"  # <- base Location = *, Astroids we see = #, astroids we dont see = x
        # pdb.set_trace()
        for asteroid in asteroid_locations.keys():
            if working_grid[asteroid] in "x*.":
                continue
            else:
                # we have a '#'
                step = asteroid[0] - base_location[0], asteroid[1] - base_location[1]
                div = gcf(step[0], step[1])
                # print(f'Base to Asteroid: {step} Compiles to: {(step[0]//div, step[1]//div)}')
                step = step[0] // div, step[1] // div

                test = asteroid[0] + step[0], asteroid[1] + step[1]
                while test in working_grid:
                    if working_grid[test] == "#":
                        working_grid[test] = "x"
                    test = test[0] + step[0], test[1] + step[1]
        asteroid_locations[base_location] = list(working_grid.values()).count("#")
        if asteroid_locations[base_location] == 282:
            print("Base Location: ", base_location)

        # printgrid(working_grid)
    return max(list(asteroid_locations.values()))


def distance(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(dx ** 2 + dy ** 2)


def angle(src, dest):

    dx = dest[0] - src[0]
    dy = dest[1] - src[1]

    if dy == 0:
        if dx > 0:
            return math.pi / 2
        return math.pi * 3 / 2

    if dx == 0:
        if dy < 0:
            return 0
        return math.pi

    if dx > 0 and dy < 0:
        return math.atan(dx / -dy)
    if dx > 0 and dy > 0:
        return math.pi / 2 + math.atan(dy / dx)
    if dx < 0 and dy > 0:
        return math.pi + math.atan(-dx / dy)
    if dx < 0 and dy < 0:
        return math.pi * 3 / 2 + math.atan(-dy / -dx)
    return math.atan(dx / -dy)


def do_angle_test():
    src = 0, 0
    dsts = [
        (0, -5),
        (2.5, -5),
        (5, -5),
        (5, 0),
        (5, 2.5),
        (5, 5),
        (0, 5),
        (-2.5, 5),
        (-5, 5),
        (-5, 0),
        (-5, -2.5),
        (-5, -5),
    ]

    dsts = []
    for x in range(8):
        dsts += [(x, -7)]

    for y in range(-7, 8):
        dsts += [(7, y)]

    for x in range(7, -8, -1):
        dsts += [(x, 7)]

    for y in range(7, -8, -1):
        dsts += [(-7, y)]

    for x in range(-7, 0):
        dsts += [(x, -7)]

    for dst in dsts:
        print(f"{src} to {dst} is angel: {angle(src,dst)}")


def dict_print(my_dict, inset_value=0):
    retval = ""
    for k, v in my_dict.items():
        retval += " " * inset_value
        retval += f"{str(k)}: {str(v)}\n"
    print(retval)


def problem2(problem_input):

    grid = dict()

    for y, line in enumerate(problem_input):
        for x, val in enumerate(line):
            grid[(x, y)] = val

    base_location = 22, 19

    asteroid_targetting = dict()

    grid[base_location] = "*"

    for asteroid in [k for k, v in grid.items() if v == "#"]:
        asteroid_targetting[asteroid] = dict()
        asteroid_targetting[asteroid]["r"] = angle(base_location, asteroid)
        asteroid_targetting[asteroid]["d"] = distance(base_location, asteroid)

    # dict_print(asteroid_targetting)

    target_order = dict()
    for k, v in asteroid_targetting.items():
        if v["r"] not in target_order:
            target_order[v["r"]] = [k]
        else:
            target_order[v["r"]] += [k]
            target_order[v["r"]].sort(key=lambda x: asteroid_targetting[x]["d"])

    dict_print(target_order)

    printgrid(grid)

    kill_order = []

    while True:
        radii_order = list(target_order.keys())
        radii_order.sort()
        for r in radii_order:
            kill_order += [target_order[r].pop(0)]
            if len(kill_order) >= 200:
                return kill_order[-1]

        target_order == {k: v for k, v in target_order.items() if len(v) > 0}

    return
    for base_location in asteroid_locations.keys():
        print(f"Investigating Astroid Base at {base_location}")
        working_grid = grid.copy()
        working_grid[
            base_location
        ] = "*"  # <- base Location = *, Astroids we see = #, astroids we dont see = x
        # pdb.set_trace()
        for asteroid in asteroid_locations.keys():
            if working_grid[asteroid] in "x*.":
                continue
            else:
                # we have a '#'
                step = asteroid[0] - base_location[0], asteroid[1] - base_location[1]
                div = gcf(step[0], step[1])
                # print(f'Base to Asteroid: {step} Compiles to: {(step[0]//div, step[1]//div)}')
                step = step[0] // div, step[1] // div

                test = asteroid[0] + step[0], asteroid[1] + step[1]
                while test in working_grid:
                    if working_grid[test] == "#":
                        working_grid[test] = "x"
                    test = test[0] + step[0], test[1] + step[1]
            asteroid_locations[base_location] = list(working_grid.values()).count("#")

        printgrid(working_grid)
    return max(list(asteroid_locations.values()))
