from helpers.all_of_them import *
from itertools import permutations
import pdb


def problem1(problem_input):

    program = [int(x) for x in problem_input.split(",")]
    c = Computer(program)

    outputs = []
    for order in permutations([0, 1, 2, 3, 4]):
        current_input = 0
        for phase_setting in order:
            c.reset()
            c.input_queue = [phase_setting, current_input]
            c.run()
            current_input = c.output_queue[0]
        outputs += [current_input]

    return max(outputs)


def problem2(problem_input):
    program = [int(x) for x in problem_input.split(",")]
    computers = [Computer(program) for _ in range(5)]
    ca = Computer(program)
    cb = Computer(program)
    cc = Computer(program)
    cd = Computer(program)
    ce = Computer(program)

    outputs = []
    for phase_settings in permutations([5, 6, 7, 8, 9]):
        for c in computers:
            c.reset()

        for i, c in enumerate(computers):
            c.input_queue = [phase_settings[i]]

        computers[0].input_queue += [0]

        while (
            not computers[0].halted
            or not computers[1].halted
            or not computers[2].halted
            or not computers[3].halted
            or not computers[4].halted
        ):

            for i, c in enumerate(computers):
                c.run()
                if len(c.output_queue) > 0:
                    next_cpu = (i + 1) % len(computers)
                    computers[next_cpu].input_queue += c.output_queue
                    c.output_queue = []

        outputs += [computers[0].input_queue[-1]]
    return max(outputs)
