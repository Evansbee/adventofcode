from helpers import *
from helpers.intcode import IntcodeComputer as Computer


def neighbor4(p):
    x, y = p[0], p[1]
    # up left right down
    return ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1))


def problem1(problem_input):
    cpu = Computer([int(x) for x in problem_input.split(",")])

    cpu.run()

    grid = dict()
    x = 0
    y = 0
    for c in cpu.output_queue:
        if c == 10:
            y += 1
            x = 0
        else:
            grid[(x, y)] = chr(c)
            x += 1

    intersections = []

    for k, v in grid.items():
        if v != "#":
            continue

        if False not in map(lambda p: grid.get(p, ".") == "#", neighbor4(k)):
            intersections += [k]

    maxx = max([x for x, y in grid.keys()]) + 1
    maxy = max([y for x, y in grid.keys()]) + 1
    for y in range(maxy):
        for x in range(maxx):
            if (x, y) in intersections:
                print("O", end="")
            else:
                if True or grid.get((x, y), ".") != ".":
                    print(grid.get((x, y), "."), end="")
                else:
                    print(" ", end="")
        print()

    return sum(map(lambda x: x[0] * x[1], intersections))


def problem2(problem_input):

    instructions = (
        "A,A,B,C,B,C,B,C,C,A\nL,10,R,8,R,8\nL,10,L,12,R,8,R,10\nR,10,L,12,R,10\ny\n"
    )
    cpu = Computer(
        [int(x) for x in problem_input.split(",")],
        [ord(x) for x in instructions],
        interactive=True,
    )
    cpu.memory[0] = 2
    while not cpu.halted:
        cpu.run()
        if cpu.awaiting_input:
            cpu.input_queue += [ord(x) for x in input()] + [ord("\n")]
            print(cpu.input_queue)
    out = "".join([chr(x) for x in cpu.output_queue if x < 255 and x > 0])

    return
