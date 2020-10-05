from helpers import *

# [Up, Right, Down, Left]

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


FACING_CODE = {"^": UP, "v": DOWN, ">": RIGHT, "<": LEFT}
LEFT_DIRECTION = {UP: LEFT, LEFT: DOWN, DOWN: RIGHT, RIGHT: UP}

RIGHT_DIRECTION = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}

OPPOSITES = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


class Square:
    def __init__(self, exits):
        self.exits = exits.copy()
        self.cart = None

    def set_cart(self, cart):
        self.cart = cart

    def intersection(self):
        if len(self.exits) > 2:
            return True
        return False

    def __str__(self):
        if self.cart:
            return self.cart.__repr__()
        if len(self.exits) == 0:
            return " "
        elif len(self.exits) == 2:
            if UP in self.exits and DOWN in self.exits:
                return "│"
            elif RIGHT in self.exits and LEFT in self.exits:
                return "─"
            elif RIGHT in self.exits and DOWN in self.exits:
                return "┌"
            elif RIGHT in self.exits and UP in self.exits:
                return "└"
            elif LEFT in self.exits and UP in self.exits:
                return "┘"
            elif LEFT in self.exits and DOWN in self.exits:
                return "┐"
            else:
                return "?"
        else:
            return "┼"

    def __repr__(self):
        if self.cart:
            return self.cart.__repr__()
        if len(self.exits) == 0:
            return " "
        elif len(self.exits) == 2:
            if UP in self.exits and DOWN in self.exits:
                return "│"
            elif RIGHT in self.exits and LEFT in self.exits:
                return "─"
            elif RIGHT in self.exits and DOWN in self.exits:
                return "┌"
            elif RIGHT in self.exits and UP in self.exits:
                return "└"
            elif LEFT in self.exits and UP in self.exits:
                return "┘"
            elif LEFT in self.exits and DOWN in self.exits:
                return "┐"
            else:
                return "?"
        else:
            return "┼"


class Cart:
    def __init__(self, position, facing):
        self.position = position
        self.facing = facing
        self.next_turn = 0
        self.last_update = -1

    def __str__(self):
        if self.facing == UP:
            return "^"
        elif self.facing == DOWN:
            return "v"
        elif self.facing == RIGHT:
            return ">"
        elif self.facing == LEFT:
            return "<"
        else:
            return "ASKDJALKSDJLAKJSDA"

    def __repr__(self):
        if self.facing == UP:
            return "^"
        elif self.facing == DOWN:
            return "v"
        elif self.facing == RIGHT:
            return ">"
        elif self.facing == LEFT:
            return "<"
        else:
            return "ASKDJALKSDJLAKJSDA"


def printgrid(grid, rows, cols):
    for y in range(rows + 1):
        for x in range(cols + 1):
            print(grid[(x, y)], end="")
        print()


def problem1(problem_input):
    return (26, 99)
    grid = dict()
    carts = []
    last_had_path = False
    num_rows = 0
    num_cols = 0

    for row, line in enumerate(problem_input):
        last_had_path = False

        for col, char in enumerate(line):
            num_cols = col
            if char == "+":
                last_had_path = True
                grid[(col, row)] = Square([UP, DOWN, LEFT, RIGHT])
            elif char == "-":
                last_had_path = True
                grid[(col, row)] = Square([LEFT, RIGHT])
            elif char == "|":
                last_had_path = False
                grid[(col, row)] = Square([UP, DOWN])

            elif char == "/":
                if last_had_path:
                    grid[(col, row)] = Square([LEFT, UP])
                    last_had_path = False
                else:
                    grid[(col, row)] = Square([DOWN, RIGHT])
                    last_had_path = True

            elif char == "\\":
                if last_had_path:
                    grid[(col, row)] = Square([LEFT, DOWN])
                    last_had_path = False
                else:
                    grid[(col, row)] = Square([UP, RIGHT])
                    last_had_path = True

            elif char == "v":
                last_had_path = False
                grid[(col, row)] = Square([UP, DOWN])
                carts.append(Cart((col, row), DOWN))
                grid[(col, row)].set_cart(carts[-1])
            elif char == "^":
                last_had_path = False
                grid[(col, row)] = Square([UP, DOWN])
                carts.append(Cart((col, row), UP))
                grid[(col, row)].set_cart(carts[-1])
            elif char == "<":
                last_had_path = True
                grid[(col, row)] = Square([LEFT, RIGHT])
                carts.append(Cart((col, row), LEFT))
                grid[(col, row)].set_cart(carts[-1])
            elif char == ">":
                last_had_path = True
                grid[(col, row)] = Square([LEFT, RIGHT])
                carts.append(Cart((col, row), RIGHT))
                grid[(col, row)].set_cart(carts[-1])
            else:
                last_had_path = False
                grid[(col, row)] = Square([])

    tick = 0
    while True:
        tick += 1
        print(tick)
        # printgrid(grid,row,col)
        for y in range(row + 1):
            for x in range(col + 1):
                if grid[(x, y)].cart and grid[(x, y)].cart.last_update < tick:
                    print(f"Cart at {(x,y)} facing {grid[(x,y)].cart.facing} ", end="")
                    if grid[(x, y)].intersection():
                        print(f"Intersection ", end="")
                        if grid[(x, y)].cart.next_turn == 0:
                            grid[(x, y)].cart.facing = LEFT_DIRECTION[
                                grid[(x, y)].cart.facing
                            ]
                        elif grid[(x, y)].cart.next_turn == 2:
                            grid[(x, y)].cart.facing = RIGHT_DIRECTION[
                                grid[(x, y)].cart.facing
                            ]

                        grid[(x, y)].cart.next_turn += 1
                        grid[(x, y)].cart.next_turn %= 3
                        print(f"now facing {grid[(x,y)].cart.facing} ", end="")
                    else:
                        facing = grid[(x, y)].cart.facing
                        way_out = [
                            x for x in grid[(x, y)].exits if x != OPPOSITES[facing]
                        ][0]
                        grid[(x, y)].cart.facing = way_out

                    next_location = (x, y)
                    if grid[(x, y)].cart.facing == UP:
                        next_location = (x, y - 1)
                    elif grid[(x, y)].cart.facing == DOWN:
                        next_location = (x, y + 1)
                    elif grid[(x, y)].cart.facing == LEFT:
                        next_location = (x - 1, y)
                    elif grid[(x, y)].cart.facing == RIGHT:
                        next_location = (x + 1, y)

                    if grid[next_location].cart:
                        return next_location
                    else:
                        print(f"moving to {next_location} ")
                        grid[(x, y)].cart.last_update = tick
                        grid[next_location].cart = grid[(x, y)].cart
                        grid[(x, y)].cart = None


def problem2(problem_input):
    grid = dict()

    last_had_path = False

    cart_count = 0

    for row, line in enumerate(problem_input):
        last_had_path = False
        for col, char in enumerate(line):
            num_cols = col
            if char == "+":
                last_had_path = True
                grid[(col, row)] = Square([UP, DOWN, LEFT, RIGHT])
            elif char == "-":
                last_had_path = True
                grid[(col, row)] = Square([LEFT, RIGHT])
            elif char == "|":
                last_had_path = False
                grid[(col, row)] = Square([UP, DOWN])

            elif char == "/":
                if last_had_path:
                    grid[(col, row)] = Square([LEFT, UP])
                    last_had_path = False
                else:
                    grid[(col, row)] = Square([DOWN, RIGHT])
                    last_had_path = True

            elif char == "\\":
                if last_had_path:
                    grid[(col, row)] = Square([LEFT, DOWN])
                    last_had_path = False
                else:
                    grid[(col, row)] = Square([UP, RIGHT])
                    last_had_path = True

            elif char == "v":
                last_had_path = False
                grid[(col, row)] = Square([UP, DOWN])
                grid[(col, row)].set_cart(Cart((col, row), DOWN))
                cart_count += 1
            elif char == "^":
                last_had_path = False
                grid[(col, row)] = Square([UP, DOWN])
                grid[(col, row)].set_cart(Cart((col, row), UP))
                cart_count += 1
            elif char == "<":
                last_had_path = True
                grid[(col, row)] = Square([LEFT, RIGHT])
                grid[(col, row)].set_cart(Cart((col, row), LEFT))
                cart_count += 1
            elif char == ">":
                last_had_path = True
                grid[(col, row)] = Square([LEFT, RIGHT])
                grid[(col, row)].set_cart(Cart((col, row), RIGHT))
                cart_count += 1
            else:
                last_had_path = False
                grid[(col, row)] = Square([])

    tick = 0
    while cart_count > 1:
        tick += 1
        for y in range(row + 1):
            for x in range(col + 1):
                if grid[(x, y)].cart and grid[(x, y)].cart.last_update < tick:

                    if grid[(x, y)].intersection():
                        if grid[(x, y)].cart.next_turn == 0:
                            grid[(x, y)].cart.facing = LEFT_DIRECTION[
                                grid[(x, y)].cart.facing
                            ]
                        elif grid[(x, y)].cart.next_turn == 2:
                            grid[(x, y)].cart.facing = RIGHT_DIRECTION[
                                grid[(x, y)].cart.facing
                            ]

                        grid[(x, y)].cart.next_turn += 1
                        grid[(x, y)].cart.next_turn %= 3

                    else:
                        facing = grid[(x, y)].cart.facing
                        way_out = [
                            x for x in grid[(x, y)].exits if x != OPPOSITES[facing]
                        ][0]
                        grid[(x, y)].cart.facing = way_out

                    next_location = (x, y)
                    if grid[(x, y)].cart.facing == UP:
                        next_location = (x, y - 1)
                    elif grid[(x, y)].cart.facing == DOWN:
                        next_location = (x, y + 1)
                    elif grid[(x, y)].cart.facing == LEFT:
                        next_location = (x - 1, y)
                    elif grid[(x, y)].cart.facing == RIGHT:
                        next_location = (x + 1, y)
                    else:
                        print("FUCKED")
                        return None

                    if grid[next_location].cart:

                        grid[next_location].cart = None
                        grid[(x, y)].cart = None
                        cart_count -= 2
                    else:
                        grid[(x, y)].cart.last_update = tick
                        grid[next_location].cart = grid[(x, y)].cart
                        grid[(x, y)].cart = None

    for y in range(row + 1):
        for x in range(col + 1):
            if grid[(x, y)].cart:
                return (x, y)
