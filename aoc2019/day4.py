from helpers import *


def irange(s, e, c=1):
    return range(s, e + 1, c)


def valid(number):
    number = [int(x) for x in str(number)]
    return len(number) == 6 and sorted(number) == number and len(set(number)) < 6


def valid2(number):
    number = [int(x) for x in str(number)]

    for i in range(10):
        if number.count(i) == 2:
            break
    else:
        return False

    return len(number) == 6 and sorted(number) == number and len(set(number)) < 6


def problem1(problem_input):

    a, b = [int(x) for x in problem_input.split("-")]
    valids = []
    for x in irange(a, b):
        if valid(x):
            valids += [x]
    return len(valids)


def problem2(problem_input):
    a, b = [int(x) for x in problem_input.split("-")]
    valids = []
    for x in irange(a, b):
        if valid2(x):
            print("Valid:", x)
            valids += [x]
    return len(valids)
