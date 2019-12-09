from helpers import *

def find_orbit_path(direct_orbits, planet, end = None):
	path = [planet]

	if planet in direct_orbits:
		if end and planet == end:

			return path
		path += find_orbit_path(direct_orbits,direct_orbits[planet],end)
	return path



def problem1(problem_input):
	direct_orbits = dict() #{Planet:Parent}

	for line in problem_input:

		parent, child = line.split(')')
		direct_orbits[child] = parent

	orbit_lengths = []
	for k in direct_orbits.keys():
		path = find_orbit_path(direct_orbits,k)
		orbit_lengths +=[len(path)-1]

	return sum(orbit_lengths)

def inf_range(start = 0, step = 1):
	while True:
		yield start
		start += step

def last_common_ancestor(a,b):
	a = a.copy()
	b = b.copy()
	a.reverse()
	b.reverse()

	last = 'COM'
	for i in inf_range():
		if a[i] == b[i]:
			last = a[i]
		else:
			return last



def problem2(problem_input):
	direct_orbits = dict() #{Planet:Parent}

	for line in problem_input:

		parent, child = line.split(')')
		direct_orbits[child] = parent

	you_path = find_orbit_path(direct_orbits,'YOU')
	san_path = find_orbit_path(direct_orbits,'SAN')


	common = last_common_ancestor(you_path,san_path)

	print(common)

	you_path = find_orbit_path(direct_orbits,'YOU',common)
	san_path = find_orbit_path(direct_orbits,'SAN',common)

	print(you_path)
	print(san_path)

	#drop 1 transfer duplicate
	san_path = san_path[:-1]
	san_path.reverse()
	transfer_path = you_path + san_path

	print("TRANSFER -> ",transfer_path)
	transfer_path = transfer_path[1:-1]
	print("TRANSFERPLAN->",transfer_path)

	return len(transfer_path)-1 #-1 because you don't need to transfer into your orbit, so it's not needed.

