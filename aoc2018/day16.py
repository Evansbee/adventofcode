from helpers import *

neumonics = [
	'ADDR',
	'ADDI',

	'MULR',
	'MULI',

	'BANR',
	'BANI',

	'BORR',
	'BORI',

	'SETR',
	'SETI',

	'GTIR',
	'GTRI',
	'GTRR',

	'EQIR',
	'EQRI',
	'EQRR'
]

opcodes = {}

def perform_operation_neumonic(reg, op): # ->[a,b,c,d]
	'''
	operation[0] is the neumonic of the opcode
	'''
	r = reg.copy()
	if op[0] == 'ADDR':
		r[op[3]] = r[op[1]] + r[op[2]]
	elif op[0] == 'ADDI':
		r[op[3]] = r[op[1]] + op[2]

	elif op[0] == 'MULR':
		r[op[3]] = r[op[1]] * r[op[2]]
	elif op[0] == 'MULI':
		r[op[3]] = r[op[1]] * op[2]

	elif op[0] == 'BANR':
		r[op[3]] = r[op[1]] & r[op[2]]
	elif op[0] == 'BANI':
		r[op[3]] = r[op[1]] & op[2]
	elif op[0] == 'BORR':
		r[op[3]] = r[op[1]] | r[op[2]]
	elif op[0] == 'BORI':
		r[op[3]] = r[op[1]] | op[2]
	elif op[0] == 'SETR':
		r[op[3]] = r[op[1]]
	elif op[0] == 'SETI':
		r[op[3]] = op[1]
	elif op[0] == 'GTIR':
		if op[1] > r[op[2]]:
			r[op[3]] = 1
		else:
			r[op[3]] = 0
	elif op[0] == 'GTRI':
		if r[op[1]] > op[2]:
			r[op[3]] = 1
		else:
			r[op[3]] = 0
	elif op[0] == 'GTRR':
		if r[op[1]] > r[op[2]]:
			r[op[3]] = 1
		else:
			r[op[3]] = 0

	elif op[0] == 'EQIR':
		if op[1] == r[op[2]]:
			r[op[3]] = 1
		else:
			r[op[3]] = 0
	elif op[0] == 'EQRI':
		if r[op[1]] == op[2]:
			r[op[3]] = 1
		else:
			r[op[3]] = 0
	elif op[0] == 'EQRR':
		if r[op[1]] == r[op[2]]:
			r[op[3]] = 1
		else:
			r[op[3]] = 0
	return r


def perform_operation(registers, operation): # ->[a,b,c,d]
	pass

def would_opcode_be_valid(precondition, operation, postcondition): # -> bool
	'''
		operation[0] should be replaced with 'command' string
	'''
	return perform_operation_neumonic(precondition,operation) == postcondition



def problem1(problem_input):
	before = []
	operation = []
	after = []
	could_bes = {}
	ops_more_than_three = 0
	for x in range(len(neumonics)):
		could_bes[x] = set(neumonics)
	#print(could_bes)
	for line in problem_input:
		if line.startswith("Before:"):
			before = all_of_them.get_numbers(line)

		elif line.startswith("After:"):
			after = all_of_them.get_numbers(line)
			#print("testing:",before,"->",operation,"->",after)
			code = operation[0]
			op_code_could_be = set()
			for n in neumonics:
				operation[0] = n
				if would_opcode_be_valid(before,operation,after):
					op_code_could_be.add(n)

			if len(op_code_could_be) >= 3:
				ops_more_than_three += 1
			could_bes[code] = could_bes[code] & op_code_could_be
		else:
			operation = all_of_them.get_numbers(line)
			#print("OP")

	return ops_more_than_three

def problem2(problem_input):
	efore = []
	operation = []
	after = []
	could_bes = {}
	ops_more_than_three = 0
	program = []
	for x in range(len(neumonics)):
		could_bes[x] = set(neumonics)

	for line in problem_input:
		if line.startswith("Before:"):
			before = all_of_them.get_numbers(line)

		elif line.startswith("After:"):
			after = all_of_them.get_numbers(line)
			program.clear()
			#print("testing:",before,"->",operation,"->",after)
			code = operation[0]
			op_code_could_be = set()
			for n in neumonics:
				operation[0] = n
				if would_opcode_be_valid(before,operation,after):
					op_code_could_be.add(n)

			if len(op_code_could_be) >= 3:
				ops_more_than_three += 1
			could_bes[code] = could_bes[code] & op_code_could_be


		elif len(line) > 0:
			operation = all_of_them.get_numbers(line)
			program += [operation]
			#print("OP")


	#figure out the opcodes...
	while len(opcodes.keys()) != len(neumonics):
		op_codes_to_close = [k for k,v in could_bes.items() if len(v) == 1]
		neumonics_to_remove = set()
		for op in op_codes_to_close:
			opcodes[op] = could_bes[op].pop()
			neumonics_to_remove.add(opcodes[op])

		for v in could_bes.values():
			v -= neumonics_to_remove

	registers = [0,0,0,0]
	for operation in program:
		operation[0] = opcodes[operation[0]]
		registers = perform_operation_neumonic(registers,operation)

	return registers[0]
