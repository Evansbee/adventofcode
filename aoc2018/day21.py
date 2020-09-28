from helpers import *

from helpers.all_of_them import *
import math

numonics = {
    4: "ADDI",
    8: "MULI",
    11: "BORR",
    9: "BORI",
    15: "MULR",
    1: "SETI",
    14: "ADDR",
    7: "GTRI",
    3: "EQRR",
    2: "EQRI",
    0: "EQIR",
    6: "GTRR",
    12: "GTIR",
    5: "SETR",
    13: "BANR",
    10: "BANI",
}
opcodes = {v: k for k, v in numonics.items()}


class CPU:
    def __init__(self, ip):
        self.registers = [0] * 6
        self.ipr = ip
        self.memory = []
        self.halted = False
        self.instructions = 0
        self.program = []
        self.breakpoints = []
        self.max = []

    def run_step(self, trace=False):
        # fetch
        if self.registers[self.ipr] >= len(self.program) or self.halted:
            self.halted = True
            return

        if self.registers[self.ipr] in self.breakpoints:

            if self.registers[5] in self.max:
                print("REPEASTTTS AFTER:",self.max[-1])
                self.halted = True
                return
            else:
                self.max += [self.registers[5]]

            print("potential answer:", self.registers[5] )


        opcode, *params = self.program[self.registers[self.ipr]]

        if trace:
            print(f"Pre: {self.registers} Op: {opcode} Params: {params}", end="")

        self.instructions += 1

        if opcode == "ADDR":
            self.registers[params[2]] = (
                self.registers[params[0]] + self.registers[params[1]]
            )
        elif opcode == "ADDI":
            self.registers[params[2]] = self.registers[params[0]] + params[1]
        elif opcode == "MULR":
            self.registers[params[2]] = (
                self.registers[params[0]] * self.registers[params[1]]
            )
        elif opcode == "MULI":
            self.registers[params[2]] = self.registers[params[0]] * params[1]
        elif opcode == "BANR":
            self.registers[params[2]] = (
                self.registers[params[0]] & self.registers[params[1]]
            )
        elif opcode == "BANI":
            self.registers[params[2]] = self.registers[params[0]] & params[1]
        elif opcode == "BORR":
            self.registers[params[2]] = (
                self.registers[params[0]] | self.registers[params[1]]
            )
        elif opcode == "BORI":
            self.registers[params[2]] = self.registers[params[0]] | params[1]
        elif opcode == "SETR":
            self.registers[params[2]] = self.registers[params[0]]
        elif opcode == "SETI":
            self.registers[params[2]] = params[0]
        elif opcode == "GTIR":
            if params[0] > self.registers[params[1]]:
                self.registers[params[2]] = 1
            else:
                self.registers[params[2]] = 0
        elif opcode == "GTRI":
            if self.registers[params[0]] > params[1]:
                self.registers[params[2]] = 1
            else:
                self.registers[params[2]] = 0
        elif opcode == "GTRR":
            if self.registers[params[0]] > self.registers[params[1]]:
                self.registers[params[2]] = 1
            else:
                self.registers[params[2]] = 0

        elif opcode == "EQIR":
            if params[0] == self.registers[params[1]]:
                self.registers[params[2]] = 1
            else:
                self.registers[params[2]] = 0
        elif opcode == "EQRI":
            if self.registers[params[0]] == params[1]:
                self.registers[params[2]] = 1
            else:
                self.registers[params[2]] = 0
        elif opcode == "EQRR":
            if self.registers[params[0]] == self.registers[params[1]]:
                self.registers[params[2]] = 1
            else:
                self.registers[params[2]] = 0
        else:
            self.halted = True

        if trace:
            print(f" Post: {self.registers}")
        self.registers[self.ipr] += 1  # 1 instruction

    def __repr__(self):
        retval = f"#IP = {self.ipr} {self.registers}"

def problem1(problem_input):
    cpu = CPU(get_numbers(problem_input.pop(0))[0])
    for line in problem_input:
        instruction, *params = line.split(" ")
        instruction = instruction.upper()
        cpu.program += [[instruction] + [int(x) for x in params]]
    cpu.registers[0] = 999999999999999999999999999999
    cpu.breakpoints += [28]
    while not cpu.halted:
        cpu.run_step(False)
        #print(cpu)
    print(cpu.registers)
    pass


def problem2(problem_input):
    print("Lets do", __file__, "problem 2")
    pass
