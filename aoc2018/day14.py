from helpers import *

def problem1(problem_input):
	elf1 = 0
	elf2 = 1

	scores = [3,7]
	while len(scores) < (int(problem_input) + 11):

		new_score = scores[elf1] + scores[elf2]
		scores += [int(x) for x in list(str(new_score))]
		elf1 = elf1 + 1 + scores[elf1]
		elf2 = elf2 + 1 + scores[elf2]

		elf1 %= len(scores)
		elf2 %= len(scores)


	return "".join([str(x) for x in scores[int(problem_input):int(problem_input)+10]])

def problem2(problem_input):
	elf1 = 0
	elf2 = 1

	scores = [3,7]
	while True:
		if (len(scores) % 100000) == 0:
			print(f'Current Length: {len(scores)}')
		new_score = scores[elf1] + scores[elf2]
		scores += [int(x) for x in list(str(new_score))]
		elf1 = elf1 + 1 + scores[elf1]
		elf2 = elf2 + 1 + scores[elf2]

		elf1 %= len(scores)
		elf2 %= len(scores)

		if len(scores) >= len(problem_input) and \
		   scores[-1] == 1 and \
		   scores[-2] == 0 and \
		   scores[-3] == 6 and \
		   scores[-4] == 3 and \
		   scores[-5] == 3 and \
		   scores[-6] == 6:
		   	return len(scores) - 6

		if len(scores) >= len(problem_input) and \
		   scores[-2] == 1 and \
		   scores[-3] == 0 and \
		   scores[-4] == 6 and \
		   scores[-5] == 3 and \
		   scores[-6] == 3 and \
		   scores[-7] == 6:
		   	return len(scores) - 7


#4086244319
