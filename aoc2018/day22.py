from helpers import *

TOOLS_FOR_TYPE = {
    0: 'CT',
    1: 'CN',
    2: 'NT'
}
def neighbor4(p,world):
    x, y, t = p[0], p[1], p[2]
    # up left right down

    at = ['C','T','N']

    at.remove(t)
    spaces = [(x, y - 1,t), (x - 1, y,t), (x + 1, y,t), (x, y + 1,t),
              (x, y,at[0]),(x, y,at[1])
              ]

    spaces = [s for s in spaces if (s[0],s[1]) in world and s[2] in TOOLS_FOR_TYPE[world[(s[0],s[1])]]]
    return tuple(spaces)


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])



def a_star(s, e, world):
    """
	s = start
	e = end
	world must support "position_clear(p) -> bool"
	todo: add different hueristics, we'll just striaght up use manahttan distnace
	"""
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
            return list(reversed(final_path)), g_score[e]

        open_set.remove(current)
        closed_set.add(current)
        for neighbor in [x for x in neighbor4(current, world)]:

            if neighbor in closed_set:
                continue

            if neighbor not in open_set:
                open_set.add(neighbor)

            # cost tries to make it prefer teh following movements UP, LEFT, RIGHT, DOWN in that order
            # don't need it, we can just search the spots for better options

            if neighbor[2] != current[2]:
                tentative_g_score = g_score[current] + 7
            else:
                tentative_g_score = g_score[current] + 1

            if neighbor in g_score and g_score[neighbor] <= tentative_g_score:
                continue  # already know better...

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + manhattan_distance(neighbor, e)
    return None, None

def print_cave(cave, current_location):
    max_y = max([y[1] for y in cave.keys()])
    max_x = max([x[0] for x in cave.keys()])

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if current_location[0] == x and current_location[1] == y:
                print('M',end='')
            else:
                print('.=|'[cave[(x,y)]],end='')
        print()

def get_cave_system(target, depth, extra = 0):
    geological_index_map = dict()
    erosion_level = dict()

    for x in range(0,target[0]+1 + extra):
        geological_index_map[(x,0)] = x * 16807
        erosion_level[(x,0)] = (geological_index_map[(x,0)] + depth) % 20183

    for y in range(1,target[1] + 1 + extra):
        geological_index_map[(0,y)] = y * 48271
        erosion_level[(0,y)] = (geological_index_map[(0,y)] + depth) % 20183


    for x in range(1,target[0]+ 1 + extra):
        for y in range(1,target[1] + 1 + extra):

            if x == target[0] and y == target[1]:
                erosion_level[(x,y)] = (0 + depth) % 20183
            else:
                geological_index_map[(x,y)] = (erosion_level[(x-1,y)]  * erosion_level[(x,y-1)])
                erosion_level[(x,y)] = (geological_index_map[(x,y)] + depth) % 20183

    cave_map = { k:(v%3) for (k,v) in erosion_level.items()}

    return cave_map


def problem1(problem_input):
    cave_system = get_cave_system((11,722),10689)
    return sum(cave_system.values())



def problem2(problem_input):
    cave_system = get_cave_system((11,722),10689,15)
    path, score = a_star((0,0,'T'),(11,722,'T'),cave_system)
    return score
