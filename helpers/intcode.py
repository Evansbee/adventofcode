import colorama
from enum import IntEnum


class OPCODE(IntEnum):
    ADD = 1
    MULT = 2
    INPUT = 3
    OUTPUT = 4
    JTRUE = 5
    JFALSE = 6
    LT = 7
    EQ = 8
    SETBASE = 9
    NOP = 98  # Custom
    HALT = 99


mnemonic_to_opcode = {
    "ADD": OPCODE.ADD,
    "MULT": OPCODE.MULT,
    "INPUT": OPCODE.INPUT,
    "OUTPUT": OPCODE.OUTPUT,
    "JT": OPCODE.JTRUE,
    "JF": OPCODE.JFALSE,
    "LT": OPCODE.LT,
    "EQ": OPCODE.EQ,
    "REBASE": OPCODE.SETBASE,
    "NOP": OPCODE.NOP,
    "HALT": OPCODE.HALT,
}

opcode_to_mnemonic = {v: k for k, v in mnemonic_to_opcode.items()}


class INSTRUCTION_MODE(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


mode_printing = {
    INSTRUCTION_MODE.POSITION: ["[", "]"],
    INSTRUCTION_MODE.IMMEDIATE: ["", ""],
    INSTRUCTION_MODE.RELATIVE: ["R{", "}"],
}

OPCODE_SIZE = {
    OPCODE.ADD: 4,
    OPCODE.MULT: 4,
    OPCODE.INPUT: 2,
    OPCODE.OUTPUT: 2,
    OPCODE.JTRUE: 3,
    OPCODE.JFALSE: 3,
    OPCODE.LT: 4,
    OPCODE.EQ: 4,
    OPCODE.SETBASE: 2,
    OPCODE.NOP: 1,
    OPCODE.HALT: 1,
}


class IntcodeComputer:
    def decode_instruction(self, position):
        instruction = self.read_mem(position)
        opcode = instruction % 100
        if opcode not in opcode_to_mnemonic:
            return -1, [], []
        positionals = [
            (instruction // (10 ** i)) % 10
            for i in range(2, 2 + OPCODE_SIZE[opcode] - 1)
        ]
        params = [
            self.read_mem(position + i + 1) for i in range(OPCODE_SIZE[opcode] - 1)
        ]
        return opcode, positionals, params

    def disasm_start_at(self, position):
        op, pos, params = self.decode_instruction(position)

        if op in opcode_to_mnemonic:
            dasm_info = {
                "start": position,
                "size": OPCODE_SIZE[op],
                "raw": [self.read_mem(position + i) for i in range(OPCODE_SIZE[op])],
                "inst": opcode_to_mnemonic[op],
                "params": [],
                "pcmatch": position == self.pc,
            }

            for i, p in enumerate(pos):
                if p == INSTRUCTION_MODE.IMMEDIATE:
                    dasm_info["params"] += [f"{params[i]}"]
                if p == INSTRUCTION_MODE.POSITION:
                    dasm_info["params"] += [f"[{params[i]}]"]
                if p == INSTRUCTION_MODE.RELATIVE:

                    dasm_info["params"] += [f"[bp+({params[i]})]"]
            return dasm_info
        else:
            dasm_info = {
                "start": position,
                "size": 1,
                "raw": [self.read_mem(position)],
                "inst": "DB",
                "params": [],
                "pcmatch": position == self.pc,
            }
            return dasm_info

    @staticmethod
    def disasm_to_string(disasm):
        max_opcode_size = max(list(OPCODE_SIZE.values()))

        raw_width = 6
        param_width = 10

        start = disasm["start"]
        raw = [f"{x:>{raw_width}}" for x in disasm["raw"]]
        if len(raw) < max_opcode_size:
            raw += [" " * raw_width] * (max_opcode_size - len(raw))
        inst = disasm["inst"]
        params = [f"{x:<{param_width}}" for x in disasm["params"]]
        if len(params) < max_opcode_size:
            params += [" " * param_width] * (max_opcode_size - len(params))

        if disasm["pcmatch"]:
            prefix = ">"
        else:
            prefix = " "
        return f'{prefix} {start:>6} | {" ".join(raw)} | {inst:<8} {" ".join(params)}'

    @staticmethod
    def disasm(program):
        return ["", ""]

    def disasm_running(self):
        pos = 0
        retval = ""
        while pos < len(self.memory):
            disasm = self.disasm_start_at(pos)
            retval += f"{IntcodeComputer.disasm_to_string(disasm)}\n"
            pos += disasm["size"]

        return retval[:-1]

    def __init__(self, memory, input_queue=[], interactive=False):
        self.initial_state = memory.copy()
        self.initial_input_queue = input_queue.copy()
        self.breakpoints = []
        self.interactive = interactive
        self.reset()

    def read_mem(self, address):
        if address < len(self.memory):
            return self.memory[address]
        return 0

    def write_memory(self, address, value):
        if address >= len(self.memory):
            self.memory.extend([0] * (1 + address - len(self.memory)))
        self.memory[address] = value

    def set_input(self, noun, verb):
        self.memory[1] = noun
        self.memory[2] = verb

    def get_op_value(self, val):
        if INSTRUCTION_MODE.IMMEDIATE:
            return val
        else:
            return self.memory[val]

    def reset(self):
        self.memory = self.initial_state.copy()
        self.input_queue = self.initial_input_queue.copy()
        self.output_queue = []
        self.pc = 0
        self.halted = False
        self.debug_mode = 0
        self.awaiting_input = False
        self.at_breakpoint = False
        self.breakpoints = []
        self.base = 0

    def get_output(self):
        return self.memory[0]

    def run_step(self, trace=False):
        self.awaiting_input = False
        self.at_breakpoint = False
        if not self.halted:
            instruction = self.memory[self.pc]
            op = instruction % 100
            positionals = [(instruction // (10 ** i)) % 10 for i in range(2, 5)]

            args = []
            arg_values = []
            arg_addrs = []

            class Param:
                def __init__(self, address, value):
                    self.a = address
                    self.v = value

            params = []

            for i in range(OPCODE_SIZE[op] - 1):
                if positionals[i] == INSTRUCTION_MODE.POSITION:
                    arg_addrs += [self.read_mem(self.pc + 1 + i)]
                elif positionals[i] == INSTRUCTION_MODE.RELATIVE:
                    arg_addrs += [self.base + self.read_mem(self.pc + 1 + i)]
                else:
                    arg_addrs += [self.pc + 1 + i]
                arg_values += [self.read_mem(arg_addrs[-1])]
                args += [self.read_mem(arg_addrs[-1])]

            self.pc += OPCODE_SIZE[op]
            if op == OPCODE.ADD:
                self.write_memory(arg_addrs[-1], args[0] + args[1])
            elif op == OPCODE.MULT:
                self.write_memory(arg_addrs[-1], args[0] * args[1])
            elif op == OPCODE.HALT:
                self.halted = True
            elif op == OPCODE.INPUT:
                if len(self.input_queue) > 0:
                    self.write_memory(arg_addrs[-1], self.input_queue[0])
                    self.input_queue = self.input_queue[1:]
                else:
                    self.awaiting_input = True
                    self.pc -= OPCODE_SIZE[op]
                    return
            elif op == OPCODE.OUTPUT:
                self.output_queue += [args[0]]
                if self.interactive:
                    if args[0] < 255:
                        print(chr(args[0]), end="")
                    else:
                        print(args[0], end="")
            elif op == OPCODE.JTRUE:
                if args[0] != 0:
                    self.pc = args[1]
            elif op == OPCODE.JFALSE:
                if args[0] == 0:
                    self.pc = args[1]
            elif op == OPCODE.LT:
                self.write_memory(arg_addrs[-1], int(args[0] < args[1]))
            elif op == OPCODE.EQ:
                self.write_memory(arg_addrs[-1], int(args[0] == args[1]))
            elif op == OPCODE.SETBASE:
                self.base += args[0]
            elif op == OPCODE.NOP:
                pass
            else:
                self.halted = True
                return

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

    def run(self, trace=False):
        self.awaiting_input = False
        while not self.halted and not self.awaiting_input:
            self.run_step(trace)
