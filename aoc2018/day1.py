from helpers import *
import re

def get_numbers_from_list(problem_input):
	return [int(x) for x in re.findall('[-+]?[0-9]+',' '.join(problem_input))]

def problem1(problem_input):
	return sum(get_numbers_from_list(problem_input))
	
	
def problem2(problem_input):
	found_frequencies = set([0])
	current_frequency = 0
	idx = 0
	num_list = get_numbers_from_list(problem_input)
	while True:
		current_frequency += num_list[idx]
		idx = (idx + 1) % len(num_list)
		if current_frequency in found_frequencies:
			return current_frequency
		else:
			found_frequencies.add(current_frequency)
	