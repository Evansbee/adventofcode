# from Advent import advent
from functools import wraps

advent_problems = []


def advent(year, day, problem):
    def inner_function(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            print(year, day, problem)
            function("PROBLEM SET")

        return wrapper

    return inner_function


@advent(2018, 12, 1)
def problem1(problem_input):
    print(problem_input)


@advent(2018, 12, 2)
def problem2(problem_input):
    print(problem_input)


for p in advent_problems:
    p("adsf")
