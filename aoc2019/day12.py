from helpers.all_of_them import *
from itertools import combinations
import time
import os


class PlanetInformation:
    def __init__(self, x, y, z, i):
        self.id = i
        self.p = [x, y, z]
        self.v = [0, 0, 0]
        print(self.id, self.p, self.v)

    def state(self):
        return (
            self.p[0] * 2
            + self.p[1] * 2
            + self.p[2] * 3
            + self.v[0] * 5
            + self.v[1] * 7
            + self.v[2] * 11
            + self.id * 13
        )

    def __repr__(self):
        return f"[{self.id}] pos=<{self.p[0]}, {self.p[1]}, {self.p[2]}>, vel=<{self.v[0]}, {self.v[1]}, {self.v[2]}>"


def pretty_planets(planets):
    _ = os.system("clear")

    for y in range(-30, 31):
        for x in range(-30, 31):
            found_planet = False
            for p in planets:
                if (x, y) == (p.p[0], p.p[1]):
                    found_planet = True
                    break
            if found_planet:
                print("*", end="")
            else:
                print(".", end="")
        print()


def problem1(problem_input):
    planets = []
    for i, line in enumerate(problem_input):
        x, y, z = get_numbers(line)
        planets += [PlanetInformation(x, y, z, i)]
    combos = list(combinations(planets, 2))
    for _ in range(1000):
        for a, b in combos:
            # print(a,b)
            for i in range(3):
                if a.p[i] > b.p[i]:
                    a.v[i] -= 1
                    b.v[i] += 1
                if a.p[i] < b.p[i]:
                    a.v[i] += 1
                    b.v[i] -= 1

        for p in planets:
            for i in range(3):
                p.p[i] += p.v[i]
        # _ = os.system('clear')
        # pretty_planets(planets)

    energy = []
    for p in planets:
        potential = sum([abs(e) for e in p.p])
        kinetic = sum([abs(e) for e in p.v])
        energy += [potential * kinetic]

    return sum(energy)


def record_state(planets, idx):

    state_list = []
    for p in planets:
        state_list += [p.p[idx]]
        state_list += [p.v[idx]]

    return tuple(state_list)


def find_cycle(planets, idx):

    state = set([record_state(planets, idx)])
    start = time.time()
    ticks = 0
    combos = list(combinations(planets, 2))
    while True:
        if (ticks % 100000) == 0:
            current_time = time.time()
            total = current_time - start
            if ticks != 0:
                per = total / ticks
                print(
                    f"{ticks} iterations complete ({total:0.2f}s - {1.0/per:0.0f} iterations/s)..."
                )
        ticks += 1
        for a, b in combos:

            if a.p[idx] > b.p[idx]:
                a.v[idx] -= 1
                b.v[idx] += 1
            elif a.p[idx] < b.p[idx]:
                a.v[idx] += 1
                b.v[idx] -= 1

        for p in planets:
            p.p[idx] += p.v[idx]

        new_state = record_state(planets, idx)
        if new_state in state:
            [print(p) for p in planets]
            return ticks
        state.add(new_state)


def factors(n):
    facs = set([1, n])
    i = 2
    while i < n ** 0.5:
        if n % i == 0:
            facs.add(n)
            facs.add(n // i)
            n = n // i
        else:
            i += 1


def gcf(*items):
    sets = []
    for i in items:
        pass


def problem2(problem_input):
    start = time.time()
    planets = []
    # problem_input = ['<x=-1, y=0, z=2>','<x=2, y=-10, z=-7>','<x=4, y=-8, z=8>','<x=3, y=5, z=-1>',	]
    for i, line in enumerate(problem_input):
        x, y, z = get_numbers(line)
        planets += [PlanetInformation(x, y, z, i)]

    x_cycle = find_cycle(planets.copy(), 0)
    y_cycle = find_cycle(planets.copy(), 1)
    z_cycle = find_cycle(planets.copy(), 2)
    for x in range(
        min(x_cycle, y_cycle, z_cycle),
        x_cycle * y_cycle * z_cycle + 1,
        min(x_cycle, y_cycle, z_cycle),
    ):
        if (x % x_cycle) == 0 and (x % y_cycle) == 0 and (x % z_cycle) == 0:
            return x
    return x_cycle * y_cycle * z_cycle
