from helpers import *
import re

def get_numbers(num_list):
	return [int(x) for x in re.matchall('-?[0-9]+',num_list)]

def problem1(problem_input):
	return sum(get_number(problem_input))
	pass
	
def problem2(problem_input):
	print('Lets do', __file__,'problem 2')
	pass