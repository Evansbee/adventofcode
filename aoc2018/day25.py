from helpers.all_of_them import get_numbers
from itertools import combinations


def get_m4(p1, p2):
    return sum([abs(p2[i] - p1[i]) for i in range(4)])


def in_constellation(constellation, star):
    for c in constellation:
        if get_m4(c, star) <= 3:
            return True
    return False


def can_constellations_combine(c1, c2):
    for s in c1:
        if in_constellation(c2, s):
            return True
    return False


def problem1(problem_input):
    print("Lets do", __file__, "problem 1")

    stars = []
    constellations = []
    for line in problem_input:
        stars += [tuple(get_numbers(line))]

    while len(stars) > 0:
        star_under_test = stars.pop(0)
        for c in constellations:
            if in_constellation(c, star_under_test):
                c += [star_under_test]
                break
        else:
            constellations += [[star_under_test]]

    combinations_happened = True
    while combinations_happened:
        print(len(constellations))
        combinations_happened = False
        i = 0
        while i < len(constellations):
            j = i + 1
            while j < len(constellations):
                if can_constellations_combine(constellations[i], constellations[j]):
                    constellations[i] += constellations[j]
                    constellations.pop(j)
                    combinations_happened = True
                j += 1
            i += 1

    return len(constellations)


def problem2(problem_input):
    print("Lets do", __file__, "problem 2")
    pass
