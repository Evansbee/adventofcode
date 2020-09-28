from helpers.intcode import *
from itertools import zip_longest

def grouper(iterable, n, fillvalue = None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def problem1(problem_input):
    cpu = IntcodeComputer([int(x) for x in problem_input.split(",")])
    grid = dict()
    cpu.run()

    for x,y,v in grouper(cpu.output_queue,3,None):
        grid[(x,y)] = v

    return len([v for v in grid.values() if v == 2])


def printgame(grid, score = 0):
    x_l = [x for x,_ in grid.keys()]
    y_l = [y for _,y in grid.keys()]
    icon = ['.','#','X','_','o']
    print("Score:",score)
    for y in range(min(y_l),max(y_l)+1):
        for x in range(min(x_l), max(x_l)+1):
            print(icon[grid[(x,y)]],end='')
        print()

def ball_and_paddle_pos(grid):
    ball = None
    paddle = None
    for p,v in grid.items():
        if v == 4:
            ball = p
        if v == 3:
            paddle = p

        if ball and paddle:
            return ball,paddle

def problem2(problem_input):
    cpu = IntcodeComputer([int(x) for x in problem_input.split(",")])
    score = 0
    grid = dict()
    cpu.memory[0] = 2
    while not cpu.halted:
        cpu.run()
        if len(cpu.output_queue) % 3 == 0:
            for x,y,v in grouper(cpu.output_queue,3,None):
                if x == -1 and y == 0:
                    score = v
                else:
                    grid[(x,y)] = v
            cpu.output_queue = []

        printgame(grid, score)

        if cpu.awaiting_input:
            b, p = ball_and_paddle_pos(grid)

            if b[0] > p[0]:
                cpu.input_queue += [ 1 ]
            elif b[0] < p[0]:
                cpu.input_queue += [-1]
            else:
                 cpu.input_queue += [0]
    return score
