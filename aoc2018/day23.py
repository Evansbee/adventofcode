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


def get_region_overlap(nanobot_dict):
    len(nanobot_dict)


def problem2(problem_input):
    nanobots = dict()
    for line in problem_input:
        x, y, z, sig = get_numbers(line)
        nanobots[(x, y, z)] = sig
    nanobots = {k: v for k, v in sorted(nanobots.items(), key=lambda item: item[1])}

    print(get_bounds(nanobots))
    print(len(nanobots))
    print(does_set_overlap(nanobots))
    return None
