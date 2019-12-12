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

    def run_step(self, trace=False):
        # fetch
        if self.registers[self.ipr] >= len(self.program) or self.halted:
            self.halted = True
            return

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
    return None
    print(problem_input)
    cpu = CPU(get_numbers(problem_input.pop(0))[0])
    for line in problem_input:
        instruction, *params = line.split(" ")
        instruction = instruction.upper()
        cpu.program += [[instruction] + [int(x) for x in params]]
    while not cpu.halted:
        cpu.run_step()
    print(cpu.registers)
    return cpu.registers[0]


fixed_input = [
    "#ip 2",
    "addi 2 16 2",
    "seti 1 1 5",
    "seti 1 1 3",
    "mulr 5 3 4",
    "eqrr 4 1 4",
    "addr 4 2 2",
    "addi 2 1 2",
    "addr 5 0 0",
    "addi 3 1 3",
    "gtrr 3 1 4",
    "addr 2 4 2",
    "seti 2 8 2",
    "addi 5 1 5",
    "gtrr 5 1 4",
    "addr 4 2 2",
    "seti 1 5 2",
    "seti 256 0 2",
    "addi 1 2 1",
    "mulr 1 1 1",
    "muli 1 209 1",
    "addi 4 3 4",
    "muli 4 22 4",
    "addi 4 7 4",
    "addr 1 4 1",
    "addr 0 2 2",
    "seti 0 4 2",
    "addi 1 10550400 1",
    "seti 0 5 0",
    "seti 0 8 2",
]


def problem2(problem_input):

    retval = set()
    a = 10551309
    # a = 100
    b = 0
    i = 1
    j = 1

    for x in range(1, int(math.sqrt(a)) + 1):
        if (a % x) == 0:
            retval.add(x)

            retval.add(a // x)
    return sum(retval)
    while True:
        b = i * j
        if b == a:
            print(f"Adding {i}")
            retval += i
        j += 1
        if j > a:
            i += 1
            if i <= a:
                j = 1
            else:
                return retval

    problem_input = fixed_input
    print(problem_input)
    cpu = CPU(get_numbers(problem_input.pop(0))[0])
    for line in problem_input:
        instruction, *params = line.split(" ")
        instruction = instruction.upper()
        cpu.program += [[instruction] + [int(x) for x in params]]

    cpu.registers[0] = 1
    r0 = [1]
    while not cpu.halted:
        # input("Enter To Continue")
        cpu.run_step(False)
        if r0[-1] != cpu.registers[0]:
            r0 += [cpu.registers[0]]
            print(r0)
    print(cpu.registers)
    return cpu.registers[0]
