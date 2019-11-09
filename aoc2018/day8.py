from helpers.all_of_them import get_numbers
import sys

class TreeNode:
	def __init__(self, name):
		self.name = name
		self.meta = []
		self.metacount = 0
		self.children = []
		self.childrencount = 0
		self.parent = None


next_node = 'A'
def update_name_node():
	global next_node
	next_node = chr(ord(next_node)+1)

def gen_next_node(generative_information):

	n = TreeNode(next_node)
	n.childrencount = generative_information.pop(0)
	n.metacount = generative_information.pop(0)
	#print(f'Generating Node: {next_node} with {n.childrencount} children and {n.metacount} metadatas (len: {len(generative_information)})')
	update_name_node()
	for _ in range(n.childrencount):
		n.children += [gen_next_node(generative_information)]
	for _ in range(n.metacount):
		n.meta += [generative_information.pop(0)]
	return n

def count_meta_datas_1(root):
	mine = sum(root.meta)

	for c in root.children:
		mine += count_meta_datas_1(c)

	return mine

def count_meta_datas_2(root):

	my_value = 0
	if root.childrencount > 0:
		for m in root.meta:
			m = m - 1
			if m >= 0 and m < root.childrencount:
				my_value += count_meta_datas_2(root.children[m])
	else:
		my_value = sum(root.meta)

	return my_value

def problem1(problem_input):
	sys.setrecursionlimit(10000)
	num_list = get_numbers(problem_input)
	root = gen_next_node(num_list)
	return count_meta_datas_1(root)


def problem2(problem_input):
	sys.setrecursionlimit(10000)
	num_list = get_numbers(problem_input)
	root = gen_next_node(num_list)
	return count_meta_datas_2(root)
