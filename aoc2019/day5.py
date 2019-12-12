from helpers.all_of_them import *


def problem1(problem_input):
    program = [int(x) for x in problem_input.split(",")]
    c = Computer(program, [1])
    c.run()
    return c.output_queue[-1]


def problem2(problem_input):
    program = [int(x) for x in problem_input.split(",")]
    c = Computer(program, [5])
    c.run()
    return c.output_queue[-1]
