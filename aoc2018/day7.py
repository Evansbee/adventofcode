from helpers import *
import re

def get_letters(line):
	return [x[0] for x in re.findall("[A-Z]\s",line)]

def problem1(problem_input):
	presteps = dict()
	for line in problem_input:
		pre, post = get_letters(line)
		if not post in presteps:
			presteps[post] = [pre]
		else:
			presteps[post] += [pre]

		#this allows us to find the one with nothing...
		if not pre in presteps:
			presteps[pre] = []

	path = ""
	while len(presteps) > 0:
		for start in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
			if start in presteps and len(presteps[start])==0:
				#found it
				path += start
				for v in presteps.values():
					if start in v:
						v.remove(start)
				presteps.pop(start, None)
				break


	return path	
	
def problem2(problem_input):
	print('Lets do', __file__,'problem 2')
	pass