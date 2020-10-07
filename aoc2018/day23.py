from helpers import *
from helpers.all_of_them import get_numbers
from itertools import combinations


def get_first_key_for_max_val(input_dict):
    max_element = max(input_dict.values())
    for k, v in input_dict.items():
        if v == max_element:
            return k


def get_bounds(input_dict):
    min_point = None
    max_point = None

    for k in input_dict.keys():
        if min_point == None:
            min_point = k
        if max_point == None:
            max_point = k

        x, y, z = k

        min_point = (min(x, min_point[0]), min(y, min_point[1]), min(z, min_point[2]))
        max_point = (max(x, max_point[0]), max(y, max_point[1]), max(z, max_point[2]))

    return min_point, max_point


def get_octree_region_bounds(a, b):
    if a[0] == b[0] and a[1] == b[1] and a[2] == b[2]:
        return []
    c = ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2, (a[2] + b[2]) // 2)

    return [
        ((a[0], a[1], a[2]), (c[0], c[1], c[2])),
        ((c[0] + 1, a[1], a[2]), (b[0], c[1], c[2])),
        ((a[0], c[1] + 1, a[2]), (c[0], b[1], c[2])),
        ((a[0], a[1], c[2] + 1), (c[0], c[1], b[2])),
        ((a[0], c[1] + 1, c[2] + 1), (c[0], b[1], b[2])),
        ((c[0] + 1, a[1], c[2] + 1), (b[0], c[1], b[2])),
        ((c[0] + 1, c[1] + 1, a[2]), (b[0], b[1], c[2])),
        ((c[0] + 1, c[1] + 1, c[2] + 1), (b[0], b[1], b[2])),
    ]


def get_manhattan_3(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1]) + abs(b[2] - a[2])


def problem1(problem_input):
    nanobots = dict()
    for line in problem_input:
        x, y, z, sig = get_numbers(line)
        nanobots[(x, y, z)] = sig

    center_location = get_first_key_for_max_val(nanobots)
    signal_strength = nanobots[center_location]
    print("Max Sig:", signal_strength)
    print("At:", center_location)
    count = 0
    in_range = [
        n
        for n in nanobots.keys()
        if get_manhattan_3(n, center_location) <= signal_strength
    ]
    return len(in_range)


def does_set_overlap(nanobot_dict):
    if len(nanobot_dict) == 1:
        return True

    all_locations = list(nanobot_dict.keys())

    while len(all_locations) > 0:
        location = all_locations[-1]
        all_locations = all_locations[:-1]
        strength = nanobot_dict[location]
        del nanobot_dict[location]
        for k, v in nanobot_dict.items():
            distance = get_manhattan_3(location, k)
            if distance > (v + strength):
                return False
    return True


def corner_points(p, r):
    return [
        (p[0] + r, p[1], p[2]),
        (p[0] - r, p[1], p[2]),
        (p[0], p[1] + r, p[2]),
        (p[0], p[1] - r, p[2]),
        (p[0], p[1], p[2] + r),
        (p[0], p[1], p[2] - r),
    ]


def neighbors(p, step=1):
    ret = []
    for x in [-step, 0, step]:
        for y in [-step, 0, step]:
            for z in [-step, 0, step]:
                if x == 0 and y == 0 and z == 0:
                    pass
                else:
                    ret += [(p[0] + x, p[1] + y, p[2] + z)]
    return ret


def problem2(problem_input):
    nanobots = dict()
    for line in problem_input:
        x, y, z, sig = get_numbers(line)
        nanobots[(x, y, z)] = sig
    nanobots = {k: v for k, v in sorted(nanobots.items(), key=lambda item: item[1])}

    all_points = []
    for k, v in nanobots.items():
        all_points += corner_points(k, v)

    best = 0
    best_points = []

    for p in all_points:
        found = 0
        for k, v in nanobots.items():
            if get_manhattan_3(p, k) <= v:
                found += 1
        if found > best:
            best_points = [p]
            best = found
        elif found == best:
            best_points += [p]

    number_of_in_range_nanobots = best
    starting_point = best_points[0]
    closest_point = starting_point
    closest_distance = get_manhattan_3((0, 0, 0), best_points[0])
    nanobots = {
        k: v for k, v in nanobots.items() if get_manhattan_3(k, starting_point) <= v
    }

    print(starting_point, closest_distance)
    to_try = [
        n
        for n in neighbors(starting_point)
        if get_manhattan_3((0, 0, 0), n) <= closest_distance
    ]
    print(to_try)
    step = 100000
    while len(to_try) > 0:
        point = to_try.pop(0)
        for k, v in nanobots.items():
            if get_manhattan_3(point, k) > v:
                break
        else:
            this_distance = get_manhattan_3((0, 0, 0), point)
            if this_distance < closest_distance:
                print("New Best Point:", point)
                closest_distance = this_distance
                closest_point = point
                to_try = [
                    n
                    for n in neighbors(point, step)
                    if get_manhattan_3((0, 0, 0), n) <= closest_distance
                ]
            else:
                to_try += [
                    n
                    for n in neighbors(point, step)
                    if get_manhattan_3((0, 0, 0), n) <= closest_distance
                ]

        if len(to_try) == 0 and step > 1:
            print("Updating Step")
            step = step // 10
            to_try = [
                n
                for n in neighbors(closest_point, step)
                if get_manhattan_3((0, 0, 0), n) <= closest_distance
            ]

    return closest_distance
