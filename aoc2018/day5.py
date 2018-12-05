from helpers import *

def react(polymer):
	i = 0
	polymer_len = len(polymer)
	while i < polymer_len-1:
		if polymer[i].lower() == polymer[i+1].lower() and polymer[i] != polymer[i+1]:
			polymer = polymer[0:i] + polymer[i+2:]
			polymer_len -= 2
			if i != 0:
				i -= 1
		else:
			i += 1
	return polymer

def problem1(problem_input):
	polymer = react(problem_input)
	return len(polymer)

	
def problem2(problem_input):
	lowest_len = len(problem_input)
	for poly in 'abcdefghijklmnopqrstuvwxyz':
		test_polymer = problem_input.replace(poly,'')
		test_polymer = test_polymer.replace(poly.upper(),'')
		test_len = len(react(test_polymer))
		lowest_len = min([lowest_len, test_len])
	return lowest_len