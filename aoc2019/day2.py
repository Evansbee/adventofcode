from helpers import *

from enum import IntEnum


class OPCODE(IntEnum):
    ADD = 1
    MULT = 2
    HALT = 99


OPCODE_SIZE = {OPCODE.ADD: 4, OPCODE.MULT: 4, OPCODE.HALT: 1}


class Computer:
    def __init__(self, program):
        self.stored_memory = program.copy()
        self.reset()

    def set_input(self, noun, verb):
        self.memory[1] = noun
        self.memory[2] = verb

    def reset(self):
        self.memory = self.stored_memory.copy()
        self.pc = 0
        self.halted = False

    def get_output(self):
        return self.memory[0]

    def run_step(self):
        if not self.halted:
            op = self.memory[self.pc]
            if op == OPCODE.ADD:
                # add
                a = self.memory[self.pc + 1]
                b = self.memory[self.pc + 2]
                dst = self.memory[self.pc + 3]
                self.memory[dst] = self.memory[a] + self.memory[b]
            elif op == OPCODE.MULT:
                # mult
                a = self.memory[self.pc + 1]
                b = self.memory[self.pc + 2]
                dst = self.memory[self.pc + 3]
                self.memory[dst] = self.memory[a] * self.memory[b]
            elif op == OPCODE.HALT:
                self.halted = True
            else:
                self.halted = True
                return
            self.pc += OPCODE_SIZE[op]

    def dump(self):
        print(f"Program Counter - {self.pc}")
        print(f"Halted ---------- {self.halted}")
        print(f"Memory Dump:")
        print(f"        ", end="")
        for i in range(16):
            print(f"       0x{i:02x}", end="")
        print()
        print("-" * 184)
        rows = (len(self.memory) // 16) + 1
        for row in range(rows):
            start_address = row * 16
            print(f"0x{start_address:04X} | ", end="")
            end_address = start_address + 16
            if end_address > len(self.memory):
                end_address = len(self.memory)

            for i in range(start_address, end_address):
                print(f"{self.memory[i]:10}", end=" ")
            print()

    def run(self):
        while not self.halted:
            self.run_step()


def problem1(problem_input):
    problem_input = [int(x) for x in problem_input.split(",")]
    computer = Computer(problem_input)
    computer.set_input(12, 2)
    computer.run()
    computer.dump()
    return computer.get_output()


def problem2(problem_input):
    problem_input = [int(x) for x in problem_input.split(",")]
    computer = Computer(problem_input)
    for noun in range(100):
        for verb in range(100):
            computer.reset()
            computer.set_input(noun, verb)
            computer.run()
            if computer.get_output() == 19690720:
                return 100 * noun + verb
    return "Failed to Get Output"
