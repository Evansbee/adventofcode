from helpers import *
from os import system
from functools import cmp_to_key
import math
answer1 = None
answer2 = None

ENEMY_TYPE = { 'G':'E', 'E':'G'}

def neighbor4(p):
	x,y = p[0],p[1]
	#up left right down
	return ((x,y-1),(x-1,y),(x+1,y),(x,y+1))

def manhattan_distance(p1,p2):
	return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def HasNeighbor(grid,p,type):
	pass


def GetAllAdjacentPositions(grid, target):
	adjacents = []
	for k,v in grid.items():
		if v['unit'] == target:
			for test_p in neighbor4(k):
				if grid[test_p]['unit'] == '.':
					adjacents += [test_p]
	return adjacents
def a_star(s, e, world):
	'''
	s = start
	e = end
	world must support "position_clear(p) -> bool"
	todo: add different hueristics, we'll just striaght up use manahttan distnace
	'''
	closed_set = set()
	open_set = set([s])
	came_from = dict()
	g_score = {s: 0}
	f_score = {s: manhattan_distance(s, e)}

	while len(open_set) > 0:

		current = min(open_set, key=lambda o: f_score[o] if o in f_score else math.inf)

		if current == e:
			final_path = [current]
			while current in came_from:
				current = came_from[current]
				final_path += [current]
			return list(reversed(final_path))

		open_set.remove(current)
		closed_set.add(current)
		for neighbor in [x for x in neighbor4(current) if world.position_clear(x)]:

			if neighbor in closed_set:
				continue

			if neighbor not in open_set:
				open_set.add(neighbor)

			#cost tries to make it prefer teh following movements UP, LEFT, RIGHT, DOWN in that order
			#don't need it, we can just search the spots for better options
			tentative_g_score = g_score[current] + 1 #reading_order_path_cost(current,neighbor)

			if neighbor in g_score and g_score[neighbor] <= tentative_g_score:
				continue  # already know better...

			came_from[neighbor] = current
			g_score[neighbor] = tentative_g_score
			f_score[neighbor] = g_score[neighbor] + manhattan_distance(neighbor, e)
	return None



def sort_position(position1, position2):
	if position1[1] != position2[1]:
		return (position1[1] > position2[1]) - (position1[1] < position2[1])
	return (position1[0] > position2[0]) - (position1[0] < position2[0])

class Unit:
	def __init__(self, unit_type, hp, ap):
		self.type = unit_type
		self.hp = hp
		self.ap = ap
		self.last_update = -1

	def __str__(self):
		return self.type

	def __repr__(self):
		return f'[Unit <type: {self.type} hp: {self.hp} ap: {self.ap} pos: {self.position}]'


class World:
	def __init__(self, elf_ap = 3):
		self.units = {}
		self.map = {}
		self.tick = 0
		self.running = True
		self.elf_deaths = 0

	def get_score(self):
		if self.running:
			return None
		else:
			goblin_health = sum([x.hp for x in self.units.values() if x.type == 'G'])
			elf_health = sum([x.hp for x in self.units.values() if x.type == 'E'])
			return (self.tick - 1) * (goblin_health + elf_health)


	def add_unit(unit, position):
		self.units[position] = [unit]

	def position_clear(self, p):
		return p not in self.units and self.map[p] == '.'

	def each_position(self):
		x_vals = [x for x,_ in self.map.keys()]
		y_vals = [y for _,y in self.map.keys()]
		for y in range(min(y_vals),max(y_vals) + 1):
			for x in range(min(x_vals), max(x_vals)+1):
				yield (x,y)

	def __str__(self):
		retval = f"World after {self.tick} tick(s)...\n\n"
		_ = system('clear')

		x_vals = [x for x,_ in self.map.keys()]
		y_vals = [y for _,y in self.map.keys()]
		retval += '              1111111111222222222233\n'
		retval += '    01234567890123456789012345678901\n'
		for y in range(min(y_vals),max(y_vals) + 1):
			retval += f'{y:>2}  '
			row_info = []
			for x in range(min(x_vals), max(x_vals)+1):
				if (x,y) in self.units:
					retval += f'{self.units[(x,y)]}'
					row_info += [f"{self.units[(x,y)]}({self.units[(x,y)].hp}[{self.units[(x,y)].ap}])"]
				else:
					retval += f'{self.map[(x,y)]}'
			retval+= f'   {", ".join(row_info)}\n'

		goblin_health = sum([x.hp for x in self.units.values() if x.type == 'G'])
		elf_health = sum([x.hp for x in self.units.values() if x.type == 'E'])
		retval += f'Total Goblin Health: {goblin_health}\n'
		retval += f'Total Elf Health: {elf_health}\n'

		if goblin_health == 0 or elf_health == 0:
			retval += f'Score: {self.get_score()}\n'

		return retval[:-1]

	def run_tick(self):
		if self.running:
			self.tick += 1
			for x,y in self.each_position():
				if (x,y) in self.units and self.units[(x,y)].last_update < self.tick:
					actual_unit_position = (x,y)
					self.units[(x,y)].last_update = self.tick
					#let's do something fun...
					my_type = self.units[(x,y)].type
					enemy_type = ENEMY_TYPE[my_type]
					enemy_positions = [k for k,v in self.units.items() if v.type == enemy_type]
					#if I have a target in range, do an attack

					if len(enemy_positions) == 0:
						self.running = False
						return

					enemy_positions_in_range = set(enemy_positions) & set(neighbor4((x,y)))
					if len(enemy_positions_in_range) == 0:
						move_to_positions = set()
						for t in enemy_positions:
							for empty in neighbor4(t):
								if self.position_clear(empty):
									move_to_positions.add(empty)
						paths = []

						for p in move_to_positions:
							best_case = manhattan_distance(actual_unit_position,p)
							if len(paths) > 0 and len(paths[0]) < best_case:
								#bail, there's no chance it's better than what we've got
								continue

							path = a_star((x,y),p,self)
							if path:
								#this includes our position, remove it
								if len(paths) > 0:
									#we already have some, is this better?
									if len(path) < len(paths[0]):
										paths.clear()
										paths += [path]
									elif len(path) == len(paths[0]):
										paths += [path]
									else:
										pass
										#this path is worse..
								else:
									paths += [path]
							else:
								pass
								#print("No Path")

						#these paths are from our position to the destination, we'll also figure out which way to go...
						if len(paths) > 0:
							#get a list of the targs

							potential_move_to_targets = list(set([p[-1] for p in paths]))
							potential_move_to_targets.sort(key=cmp_to_key(sort_position))

							move_to_target = potential_move_to_targets[0]

							#find the best path for us UP, LEFT, RIGHT, DOWN
							#neighbors 4 gives us this order:
							move_path = None
							for potential_first_move in neighbor4(actual_unit_position):
								if self.position_clear(potential_first_move):
									path = a_star(potential_first_move,move_to_target,self)

									if not move_path and path:
										move_path = path
									if path and move_path and len(path) < len(move_path):
										move_path = path

							next_move = move_path[0]
							u = self.units[(x,y)]
							del(self.units[(x,y)])
							self.units[next_move] = u
							actual_unit_position = next_move

					enemy_positions_in_range = set(enemy_positions) & set(neighbor4(actual_unit_position))
					if len(enemy_positions_in_range) > 0:
						enemy_positions_in_range = list(enemy_positions_in_range)
						enemy_positions_in_range.sort(key=lambda u: self.units[u].hp)
						enemy_unit = self.units[enemy_positions_in_range[0]]
						enemy_unit.hp -= self.units[actual_unit_position].ap
						if enemy_unit.hp <= 0:
							if enemy_unit.type =='E':
								self.elf_deaths += 1
							del(self.units[enemy_positions_in_range[0]])


	def run_until_end(self):
		while self.running:
			self.run_tick()



def problem1(problem_input):
	world = World()
	for y,line in enumerate(problem_input):
		for x,char in enumerate(line):
			if char in ['.', '#']:
				world.map[(x,y)] = char
			elif char in ['G','E']:
				world.map[(x,y)] = '.'
				world.units[(x,y)] = Unit(char,200,3)
			else:
				print("FAIL")


	while(world.running):
		print(world)
		world.run_tick()
	return world.get_score()

def problem2(problem_input):
	for test_ap in range(1000000):
		world = World()
		for y,line in enumerate(problem_input):
			for x,char in enumerate(line):
				if char in ['.', '#']:
					world.map[(x,y)] = char
				elif char == 'G':
					world.map[(x,y)] = '.'
					world.units[(x,y)] = Unit(char,200,3)
				elif char == 'E':
					world.map[(x,y)] = '.'
					world.units[(x,y)] = Unit(char,200,test_ap)
				else:
					print("FAIL")


		while(world.running):
			print(world)
			world.run_tick()
			if world.elf_deaths > 0:
				break

		if not world.running and world.elf_deaths == 0:
			return world.get_score()

