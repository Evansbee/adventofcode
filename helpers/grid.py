class Grid:
    def __init__(self, default_entry=0):
        self.grid = dict()
        self.default = default_entry
        self.max_set = False
        self.min_x = None
        self.min_y = None
        self.max_x = None
        self.max_y = None

    def x_range(self):
        return range(self.x_min, self.x_max + 1)

    def y_range(self):
        return range(self.y_min, self.y_max + 1)

    def get(self, x, y):
        self.grid.get((x, y), self.default)

    def set(self, x, y, val):
        self.grid[(x, y)] = val
        if not self.max_set:
            self.x_max = x
            self.x_min = x
            self.y_max = y
            self.y_min = y
            self.max_set = True

        self.x_max = max(x, self.x_max)
        self.y_max = max(y, self.y_max)
        self.x_min = min(x, self.x_min)
        self.y_min = min(y, self.y_min)

    def print(self, print_map=None):
        if print_map == None:
            print_map = {0: " ", 1: "#"}

        for y in self.y_range():
            line = ""
            for x in self.x_range():
                val = self.get(x, y)
                if val in print_map:
                    line += print_map[self.get(x, y)]
                else:
                    line += "?"
            print(line)
