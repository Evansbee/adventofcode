from helpers.all_of_them import get_numbers

def y_sep(grid):
	min_y = grid[0]['p'][1]
	max_y = min_y
	for p in grid:
		min_y = min(min_y, p['p'][1])
		max_y = max(max_y, p['p'][1])

	return max_y - min_y

def printgrid(grid):
	min_y = grid[0]['p'][1]
	max_y = min_y
	min_x = grid[0]['p'][0]
	max_x = min_x
	for p in grid:
		min_y = min(min_y, p['p'][1])
		max_y = max(max_y, p['p'][1])
		min_x = min(min_x, p['p'][0])
		max_x = max(max_x, p['p'][0])

	for y in range(min_y,max_y + 1):
		for x in range(min_x,max_x + 1):
			for p in grid:
				if p['p'][0] == x and p['p'][1] == y:
					print('#',end='')
					break
			else:
				print(' ',end='')
		print()


def tick(grid, steps = 1):
	for p in grid:
		p['p'][0] += steps * p['v'][0]
		p['p'][1] += steps * p['v'][1]

def problem1(problem_input):
	grid = []
	t = 0
	for line in problem_input:
		nums = get_numbers(line)
		star = { 'p': [nums[0], nums[1]], 'v':[nums[2],nums[3]]}
		grid += [star]

	while y_sep(grid) > 9:
		tick(grid)

	printgrid(grid)
	return None
	
def problem2(problem_input):
	grid = []
	t = 0
	for line in problem_input:
		nums = get_numbers(line)
		star = {'p': [nums[0], nums[1]], 'v': [nums[2], nums[3]]}
		grid += [star]

	while y_sep(grid) > 9:
		t += 1
		tick(grid)

	return t
