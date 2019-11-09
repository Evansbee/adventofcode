from helpers import *

def get_value_for_position(x,y, sn):
	rackid = x + 10
	powerlevel = rackid * y
	powerlevel += sn
	powerlevel *= rackid
	if powerlevel > 100:
		powerlevel = int(str(powerlevel)[-3])
	else:
		powerlevel = 0
	powerlevel -= 5
	return powerlevel




def problem1(problem_input):
	thegrid = dict()
	problem_input = int(problem_input)
	for x in range(1,301):
		for y in range(1,301):
			thegrid[(x,y)] = get_value_for_position(x,y,problem_input)

	start = (0,0)
	value = -100000
	for sx in range(1,301-3):
		for sy in range(1,301-3):
			test_value = 0;
			for x in range(sx,sx+3):
				for y in range(sy,sy+3):
					test_value += thegrid[(x,y)]
			if test_value > value:
				value = test_value
				start = (sx, sy)
	return start
	
def problem2(problem_input):
	thegrid = dict()
	problem_input = int(problem_input)
	for x in range(1, 301):
		for y in range(1, 301):
			thegrid[(x, y, 1)] = get_value_for_position(x, y, problem_input)


	for x in range(1,301):
		print(f'Processing row {x}')
		for y in range(1,301):
			for grid_size in range(2, 301):
				if x + grid_size > 301 or y + grid_size > 301:
					break

				thegrid[(x, y, grid_size)] = thegrid[(x, y, grid_size-1)]

				try:
					for testx in range(x,x+grid_size):
						thegrid[(x, y, grid_size)] += thegrid[(testx,y+grid_size-1,1)]

					for testy in range(y,y + grid_size - 1):
						thegrid[(x, y, grid_size)] += thegrid[(x+grid_size - 1, testy , 1)]
				except Exception as inst:
					print("EXCEPTION")

	start = (0, 0, 1)
	value = -100000
	for k, v in thegrid.items():
		if v > value:
			start = k
			value = v

	return start