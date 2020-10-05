# from helpers import *
from itertools import chain, product
import time


def pattern(pattern: list, offset: int):
    pattern = [pattern] * (offset + 1)
    pattern = [item for sublist in zip(*pattern) for item in sublist]
    current = 1
    while True:
        yield pattern[current]
        current = (current + 1) % len(pattern)


def fft_for_digit(i, array):
    start = i
    step = i + 1
    val = 0

    for outer in range(start, len(array), step * 4):
        end = min(len(array), outer + step)
        val += sum(array[outer:end])
        end = min(len(array), outer + step * 3)
        val -= sum(array[outer + step * 2 : end])

    return abs(val) % 10


def do_fft(number_list, p2=False):

    np = [0] * len(number_list)
    last = 0
    for i in range(len(number_list) - 1, len(number_list) // 2, -1):
        np[i] = (number_list[i] + last) % 10
        last = np[i]

    if p2:
        return np
    for i in range(len(number_list) // 2 + 1):
        np[i] = fft_for_digit(i, number_list)

    return np


sig = 0


def problem1(problem_input):

    fftcount = 100
    problem_input = [int(x) for x in problem_input]

    for _ in range(fftcount):
        problem_input = do_fft(problem_input)
        # print("".join([str(x) for x in problem_input[600:]]))

    return "".join([str(x) for x in problem_input[:8]])


def problem2(problem_input):

    fftcount = 100
    offset = int(problem_input[:7])
    problem_input = [int(x) for x in problem_input] * 10000

    start = time.time()
    for x in range(fftcount):

        problem_input = do_fft(problem_input, True)
        # print("".join([str(x) for x in problem_input[-50:]]))
    # offset = "".join([str(x) for x in problem_input[:7]])
    return "".join([str(x) for x in problem_input[offset : offset + 8]])
