from helpers import *


class Tree:
    def __init__(self):
        self.commands = ""
        self.children = []
        self.parent = None

    def append_path(self, char):
        if len(self.children) == 0:
            self.commands += char
        for c in self.children:
            c.append_path(char)

    def make_string(self, indent=0):
        retval = (" " * indent) + f"{self.commands}\n"
        for c in self.children:
            retval += c.make_string(indent + 2)
        return retval

    def __str__(self):
        return self.make_string()

    def __repr__(self):
        return self.make_string()

    def make_all_full_paths(self):
        pass


def populate_children(head, roommap):
    while True:
        if len(roommap) == 0:
            return

        char = roommap.pop(0)
        if char not in "^(|)$":
            head.append_path(char)
        elif char == "(":
            head.children += [Tree()]
            head.children[-1].parent = head
            populate_children(head.children[-1], roommap)
        elif char == ")":
            return
        elif char == "|":
            head.parent.children += [Tree()]
            head.parent.children[-1].parent = head
            head = head.parent.children[-1]


def problem1(problem_input):
    head = Tree()
    head.children = [Tree()]
    head.children[-1].parent = head
    problem_input = list(problem_input)
    populate_children(head.children[-1], problem_input)
    print(head)
    pass


def problem2(problem_input):
    print("Lets do", __file__, "problem 2")
    pass
