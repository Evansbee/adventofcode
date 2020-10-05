from helpers import *
from random import randint
import sys

sys.setrecursionlimit(10000)

DIRECTIONS = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}


class Node:
    next_id = 0

    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent

        self.max_path = 0
        self.distance_from_start = 0
        self.children = []
        self.closing_item = None
        self.descendents = []
        self.id = Node.next_id
        self.potential_node_locations_with_distance = dict()
        Node.next_id += 1

    def __len__(self):
        if self.data in "()|^$":
            return 0
        return len(self.data)

    def is_control(self):
        return self.data in ("()|^$")

    def give_child_to_dead_ends(self, child):
        for c in self.descendents:
            if len(c.children) == 0:
                for k, v in c.potential_node_locations_with_distance.items():
                    if (
                        k not in child.potential_node_locations_with_distance
                        or v < child.potential_node_locations_with_distance[k]
                    ):
                        child.potential_node_locations_with_distance[k] = v
                c.children = [child]
        self.closing_item = child
        self.max_path = self.max_len_sub_paths(True)

    def print_all_paths(self, start=""):
        paths = []
        my_contribution = self.data.strip("$^()|")
        if len(self.children) == 0:
            return [start + my_contribution]
        else:
            for c in self.children:
                paths += c.print_all_paths(start + my_contribution)
        return paths

    def max_len_sub_paths(self, force_start=False):
        if len(self.data) > 0 and self.data in "(^" and not force_start:
            if self.closing_item is not None:
                path_lengths = [
                    x.max_len_sub_paths() for x in self.closing_item.children
                ]
                if 0 in path_lengths:
                    return self.max_path
                return self.max_path + max(path_lengths + [0])

        path_lengths = [x.max_len_sub_paths() for x in self.children]
        if 0 in path_lengths:
            return len(self)
        return len(self) + max(path_lengths + [0])

    def map_rooms_to_distance(
        self, room_distance=None, current_distance=None, current_room=None
    ):
        starting = room_distance == None
        if room_distance == None:
            room_distance = dict()
            current_distance = 0
            current_room = (0, 0)
        # print(self)
        if not self.is_control():
            thing = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}
            current_distance += 1
            current_room = (
                current_room[0] + thing[self.data][0],
                current_room[1] + thing[self.data][1],
            )

            if (
                current_room not in room_distance
                or room_distance[current_room] > current_distance
            ):
                room_distance[current_room] = current_distance

        for c in self.children:
            c.map_rooms_to_distance(room_distance, current_distance, current_room)

        if starting:
            return room_distance

    def __repr__(self):
        return (
            f"NODE: {self.data} Children: {[x.data for x in self.children]} ({self.id})"
        )


def get_next_token_from_string(input_string):
    return input_string[0], input_string[1:]
    if input_string[0] in "()|$^":
        return input_string[0], input_string[1:]
    else:
        token = ""
        while input_string[0] not in "()|$^":
            token = token + input_string[0]
            input_string = input_string[1:]
        return token, input_string


def make_graph(input_string):
    all_nodes = []
    head = None
    current = None
    stack = []
    initial_string_length = len(input_string)
    big_list = []
    while len(input_string) > 0:
        token, input_string = get_next_token_from_string(input_string)
        # print(f'Progress: {((initial_string_length-len(input_string))/initial_string_length)*100:2f}% Stack Depth: {len(stack)} Token: {token}')
        if token == "^":
            head = Node("^")
            head.potential_node_locations_with_distance[(0, 0)] = 0

            current = head
            current.min_prefix = 0
            current.min_prefix = 0
            stack = [head]

        elif token == "(":
            current.children += [Node("(")]
            stack[-1].descendents += [current.children[-1]]
            stack += [current.children[-1]]
            current.children[
                -1
            ].potential_node_locations_with_distance = (
                current.potential_node_locations_with_distance.copy()
            )
            current = current.children[-1]

        elif token == ")":
            temp = Node(")")
            stack[-1].give_child_to_dead_ends(temp)

            stack = stack[:-1]
            current = temp
            stack[-1].descendents += [current]

        elif token == "|":
            stack[-1].children += [Node("")]
            current = stack[-1].children[-1]
            current.potential_node_locations_with_distance = stack[
                -1
            ].potential_node_locations_with_distance.copy()
            stack[-1].descendents += [current]
        elif token == "$":
            temp = Node("$")
            stack[-1].give_child_to_dead_ends(temp)
            return head, all_nodes
        else:
            current.children += [Node(token)]
            for k, v in current.potential_node_locations_with_distance.items():
                new_location = (
                    k[0] + DIRECTIONS[token][0],
                    k[1] + DIRECTIONS[token][1],
                )
                current.children[-1].potential_node_locations_with_distance[
                    new_location
                ] = (v + 1)

            current = current.children[-1]
            stack[-1].descendents += [current]
            all_nodes += [current]

    return head, all_nodes


def test():

    return None


def problem1(problem_input):
    head, _ = make_graph(problem_input)
    return head.max_path


def problem2(problem_input):
    head, all_nodes = make_graph(problem_input)
    print(all_nodes)
    map_to_nodes = dict()

    for node in all_nodes:
        for k, v in node.potential_node_locations_with_distance.items():
            if k not in map_to_nodes or map_to_nodes[k] > v:
                map_to_nodes[k] = v

    map_to_nodes = {k: v for (k, v) in map_to_nodes.items() if v >= 1000}

    return len(map_to_nodes.keys())
