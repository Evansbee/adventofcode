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

	time = 0
	working_set = dict()
	while len(presteps) > 0:
		for start in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
			if start in presteps and len(presteps[start])==0 and len(working_set) < 5:
				working_set[start] = ord(start) - ord('A') + 61

		lowest = min(working_set.items(), key = lambda x: x[1])
		time += lowest[1]
		working_set.pop(lowest[0],None)
		for k in working_set.keys():
			working_set[k]-=lowest[1]

		for v in presteps.values():
			if lowest[0] in v:
				v.remove(lowest[0])
		presteps.pop(lowest[0], None)
		
	return time	

	#SetTimeToCompleteForAllCompletables
	#rmove lowest time to complete from all items
	#add item to queue
	#again