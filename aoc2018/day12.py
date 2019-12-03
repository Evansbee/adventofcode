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

	for i,v in enumerate(initial_string):
		if v != '.':
			plants[i] = v

	for i in range(20):

		minvalue = min(plants.keys()) - 3
		maxvalue = max(plants.keys()) + 3
		newplants = defaultdict(lambda: '.')

		for i in range(minvalue,maxvalue+1):
			newplants[i] = translations[get_surrounding_area(plants,i)]

		plants.clear()
		for k,v in newplants.items():
			if v != '.':
				plants[k] = v

		print(i, sum(plants.keys()))
	return sum(plants.keys())

def problem2(problem_input):
	plants = defaultdict(lambda: '.')
	translations = dict()
	initial_string = problem_input[0].split(": ")[-1]

	problem_input = problem_input[2:]
	for line in problem_input:
		start, end = line.split(" => ")
		translations[start] = end

	for i,v in enumerate(initial_string):
		if v != '.':
			plants[i] = v

	for x in range(5000):

		minvalue = min(plants.keys()) - 3
		maxvalue = max(plants.keys()) + 3
		newplants = defaultdict(lambda: '.')

		for i in range(minvalue,maxvalue+1):
			newplants[i] = translations[get_surrounding_area(plants,i)]

		plants.clear()
		for k,v in newplants.items():
			if v != '.':
				plants[k] = v

		print(x, sum(plants.keys()))

	#it stablizes to increase by 102 so i just did the math after 5000
	return sum(plants.keys())
