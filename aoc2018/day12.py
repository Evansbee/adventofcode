from helpers import *
from collections import defaultdict

def get_surrounding_area(plants, position):
	return f'{plants[position-2]}{plants[position-1]}{plants[position]}{plants[position+1]}{plants[position+2]}'


def problem1(problem_input):
	plants = defaultdict(lambda: '.')
	translations = dict()
	initial_string = problem_input[0].split(": ")[-1]

	problem_input = problem_input[2:]
	for line in problem_input:
		start, end = line.split(" => ")
		translations[start] = end
	print(problem_input)
	print(translations)
	for _ in range(20):

		newplants = defaultdict(lambda: '.')
		plants = newplants.copy()

	return plants

def problem2(problem_input):
	print('Lets do', __file__,'problem 2')
	pass
