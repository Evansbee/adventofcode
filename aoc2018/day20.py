from helpers import *


class Tree:
    def __init__(self, parent = None, remaining = ""):
        self.remaining = remaining
        self.commands = ""
        self.children = []
        self.parent = parent

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

        my_list = []
        for c in self.children:
            my_list += c.make_all_full_paths()

        if len(my_list) == 0:
            my_list = [""]


        for i,l in enumerate(my_list):
            my_list[i] = self.commands + l

        return my_list

    def make_sibling(self, remaining = ""):
        sib = Tree(self.parent, remaining)
        self.parent.children += [sib]
        return sib

    def dirs_left(self):
        if not self.parent:
            return len(self.remaining)
        else:
            return self.parent.dirs_left()

    def get_next_dir(self):

        if not self.parent:
            char = self.remaining[0]
            self.remaining = self.remaining[1:]
            return char
        else:
            return self.parent.get_next_dir()


    def populate_down(self):
        while True:
            if self.dirs_left() == 0:
                return

            char = self.get_next_dir()
            #print(f'Processing: {char}')

            if char not in "^(|)$":
                #print('Appending to self')
                self.append_path(char)

            elif char == "(":
                #print('Adding Child')
                if len(self.children) > 0:
                    pass
                else:
                    self.children += [Tree(self)]
                    self.children[-1].populate_down()
            elif char == ")":
                return
            elif char == "|":
                #print('spawning sibling')
                sib = self.make_sibling()
                sib.populate_down()
                return
            elif char == "^":
                pass
            elif char == '$':
                return

'''
add self
add self
(
    add child
    add to child
    |
    get child
    addd
    (
        make child deal with it
    )
    add child
    add child
)
add self -> push down
'''



def test():





    test_input = "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"
    head = Tree(None, test_input)
    head.populate_down()
    print("TEST INPUT:",test_input)
    [print(l) for l in head.make_all_full_paths()]
    print(max([len(l) for l in head.make_all_full_paths()]))


    test_input = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"
    head = Tree(None, test_input)
    head.populate_down()
    print("TEST INPUT:",test_input)
    [print(l) for l in head.make_all_full_paths()]
    print(max([len(l) for l in head.make_all_full_paths()]))


    test_input = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
    head = Tree(None, test_input)
    head.populate_down()
    print("TEST INPUT:",test_input)
    [print(l) for l in head.make_all_full_paths()]
    print(max([len(l) for l in head.make_all_full_paths()]))

    return max([len(l) for l in head.make_all_full_paths()])

def problem1(problem_input):
    return None
    head = Tree(None, problem_input)
    head.populate_down()
    #[print(l) for l in head.make_all_full_paths()]
    return max([len(l) for l in head.make_all_full_paths()])



def problem2(problem_input):
    print("Lets do", __file__, "problem 2")
    pass
