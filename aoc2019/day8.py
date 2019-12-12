from helpers import *


def problem1(problem_input):
    items = list(problem_input)
    image = dict()
    layer = 0
    while len(items) > 0:
        for y in range(6):
            for x in range(25):
                image[(x, y, layer)] = int(items.pop(0))
        layer += 1

    layer_list = dict()
    direct_calc = dict()
    for z in range(layer):
        layer_list[z] = []
        direct_calc[z] = 0
        for y in range(6):
            for x in range(25):
                layer_list[z] += [image[(x, y, z)]]
                if image[(x, y, z)] == 0:
                    direct_calc[z] += 1

    layer_to_investigate = [
        k for k, v in direct_calc.items() if v == min(direct_calc.values())
    ][0]

    return layer_list[layer_to_investigate].count(1) * layer_list[
        layer_to_investigate
    ].count(2)


def problem2(problem_input):
    items = list(problem_input)
    image = dict()
    layer = 0

    compiled_image = dict()
    while len(items) > 0:
        for y in range(6):
            for x in range(25):
                image[(x, y, layer)] = int(items.pop(0))
                if image[(x, y, layer)] != 2 and (x, y) not in compiled_image:
                    compiled_image[(x, y)] = image[(x, y, layer)]
        layer += 1

    for y in range(6):
        for x in range(25):
            print(f'{[" ","#"][compiled_image[(x,y)]]}', end="")
        print()
    return "READ ABOVE"
