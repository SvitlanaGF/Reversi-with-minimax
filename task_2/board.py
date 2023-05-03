class Board:
    def __init__(self, cols):
        self.cols = cols

    def print_grid(self):
        print('  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |')
        for i, row in enumerate(self.grid()):
            line = f'{i} |'.ljust(3, " ")
            for item in row:
                line += f'{item}'.center(3, ' ') + '|'
            print(line)
        print()

    def grid(self):
        grid_ = []
        for y in range(self.cols):
            line = []
            for x in range(self.cols):
                line.append(0)
            grid_.append(line)
        return grid_
