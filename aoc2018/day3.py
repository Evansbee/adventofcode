from helpers import *
from collections import defaultdict
import re


def get_numbers(line):
    return [int(x) for x in re.findall("[0-9]+", line)]


def problem1(problem_input):
    grid = defaultdict(list)
    for line in problem_input:
        case, x, y, width, height = get_numbers(line)
        for _x in range(x, x + width):
            for _y in range(y, y + height):
                grid[(_x, _y)] += [case]

    dupes = [v for v in grid.values() if len(v) > 1]
    return len(dupes)


def problem2(problem_input):
    grid = defaultdict(list)
    all_claims = set()
    for line in problem_input:
        case, x, y, width, height = get_numbers(line)
        all_claims.add(case)
        for _x in range(x, x + width):
            for _y in range(y, y + height):
                grid[(_x, _y)] += [case]

    dupes = [v for v in grid.values() if len(v) > 1]
    invalid_claims = set()
    for bad_square in dupes:
        for c in bad_square:
            invalid_claims.add(c)

    return list(all_claims.difference(invalid_claims))[0]
