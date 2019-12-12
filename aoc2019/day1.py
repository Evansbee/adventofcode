from helpers import *


def problem1(problem_input):
    fuel = [int(x) // 3 - 2 for x in problem_input]
    return sum(fuel)


def fuel_value(mass):
    fuel = int(mass) // 3 - 2
    if fuel < 0:
        return 0
    return fuel


def problem2(problem_input):
    masses = problem_input
    total = 0
    while len(masses) > 0:
        masses = [fuel_value(x) for x in masses]
        total += sum(masses)
        masses = list(filter((0).__ne__, masses))
    return total
