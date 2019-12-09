from helpers import *
from collections import defaultdict

'''
my test...
            11111111112
  012345678901234567890
0 ..........+..........
1 .....................
2 ..#......###......#..
3 ..#...............#..
4 ..#...........#...#..
5 ..#...#.......#...#..
6 ..#...#########...#..
7 ..#...............#..
8 ..#################..
.....................
'''

test_input = '''x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504'''.split('\n')


def below(p):
	return (p[0],p[1]+1)

def left(p):
	return (p[0]-1,p[1])

def right(p):
	return (p[0]+1,p[1])

def printgrid(grid):
	min_x = min([x for x,y in grid.keys()])
	max_x = max([x for x,y in grid.keys()])
	min_y = min([y for x,y in grid.keys()])
	max_y = max([y for x,y in grid.keys()])

	for y in range(min_y, max_y + 1):
		print(f'{y:>6}  ', end='')
		for x in range(min_x, max_x +1):
			if (x,y) in grid:
				print(grid[(x,y)], end ='')
			else:
				print('.', end ='')
		print()


#needs to be horizontal or vertical...
def fill_h_line(grid, x1, x2, y, val):
	for x in range(x1,x2+1):
		grid[(x,y)] = val

def fill_v_line(grid, x, y1, y2, val):
	for y in range(y1,y2+1):
		grid[(x,y)] = val

def find_next_non_free_below(grid, pos,max_y,okvals = '.|'):
	for y in range(pos[1]+1,max_y+1):
		if (pos[0],y) not in grid or grid[(pos[0],y)] in okvals:
			continue
		return (pos[0],y)
	return (pos[0],max_y)


def directions_water_can_flow_from_here(grid, position):
	res = []
	positions = [left(position),right(position),below(position)]
	for p in positions:
		if p not in grid or grid[p] in '.|F':
			res += [p]
	return res


def find_pool_extremes(grid, position):
	l, r = position , position

	while True:
		if below(l) in directions_water_can_flow_from_here(grid, l):
			break
		elif left(l) in directions_water_can_flow_from_here(grid, l):
			l = left(l)
		else:
			break

	while True:
		if below(r) in directions_water_can_flow_from_here(grid, r):
			break
		elif right(r) in directions_water_can_flow_from_here(grid, r):
			r = right(r)
		else:
			break

	return l,r




def problem1(problem_input):
	cursor = [(500,0)]
	#cursor = [(10,0)]
	grid = dict()
	problem_input = test_input
	#print(problem_input)
	for line in problem_input:
		numbers = all_of_them.get_numbers(line)
		for v in range(numbers[1],numbers[2]+1):
			if line[0] == 'x':
				grid[(numbers[0],v)] = '#'
			else:
				grid[(v,numbers[0])] = '#'

	min_x = min([x for x,y in grid.keys()])
	max_x = max([x for x,y in grid.keys()])
	min_y = min([y for x,y in grid.keys()])
	max_y = max([y for x,y in grid.keys()])



	while len(cursor) > 0:
		current_spout = cursor[-1]
		cursor = cursor[:-1]

		todown = below(current_spout)
		toleft = left(current_spout)
		toright = right(current_spout)


		if todown[1] > max_y:
			grid[current_spout] = 'F'
		elif todown not in grid or grid[todown] in '.':
			grid[current_spout] = '|'
			cursor += [current_spout] #keep this there to go back up
			cursor += [todown]
		elif grid[todown] in '#~':
			grid[current_spout] = '|'

			l,r = find_pool_extremes(grid,current_spout)

			if below(l) not in directions_water_can_flow_from_here(grid,l) and below(r) not in directions_water_can_flow_from_here(grid,r):
				fill_h_line(grid,l[0],r[0],current_spout[1],'~')
			else:
				fill_h_line(grid,l[0],r[0],current_spout[1],'|')
				if below(l) in directions_water_can_flow_from_here(grid,l):
					cursor += [l]

				if below(r) in directions_water_can_flow_from_here(grid,r):
					cursor += [r]
		elif grid[todown] in 'F':
			grid[current_spout] = 'F'

		cursor = [x for x in cursor if x[1] <= max_y]
		#printgrid(grid)

	printgrid(grid)
	waters = [v for k,v in grid.items() if k[1] <= max_y and k[1] >= min_y and v in '|.F~']


	return len(waters)

def problem2(problem_input):
	print('Lets do', __file__,'problem 2')
	pass
