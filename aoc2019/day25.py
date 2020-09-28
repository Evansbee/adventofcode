from helpers import *
from helpers.intcode import IntcodeComputer as Computer

def problem1(problem_input):
    cpu = Computer([int(x) for x in problem_input.split(',')],interactive=True)
    while not cpu.halted:
        cpu.run()
        if cpu.awaiting_input:
            cpu.input_queue += [ord(x) for x in input()] + [ord('\n')]
    return


def problem2(problem_input):
    return None
