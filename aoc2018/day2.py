from helpers import *
from collections import defaultdict


def day2algo1(line):
    has_two = False
    has_three = False
    count = defaultdict(int)
    for char in line:
        count[char] += 1

    for v in count.values():
        if v == 2:
            has_two = True

        if v == 3:
            has_three = True
    return (has_two, has_three)


def differs_by(in1, in2):
    different_items = 0
    for i in range(len(in1)):
        if in1[i] != in2[i]:
            different_items += 1
    return different_items


def combine_sames(in1, in2):
    out = ""
    for i in range(len(in1)):
        if in1[i] == in2[i]:
            out += in1[i]
    return out


def day2algo2(lines):
    for i in range(len(lines)):
        for j in range(len(lines)):
            if i != j:
                if differs_by(lines[i], lines[j]) == 1:
                    return combine_sames(lines[i], lines[j])
    return ""


def problem1(problem_input):
    twos = 0
    threes = 0
    for line in problem_input:
        (a, b) = day2algo1(line)
        if a:
            twos += 1
        if b:
            threes += 1
    return twos * threes


def problem2(problem_input):
    return day2algo2(problem_input)
