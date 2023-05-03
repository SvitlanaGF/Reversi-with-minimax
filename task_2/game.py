from board import Board
from algorithm import *


class Reversi:
    def __init__(self):
        self.board = Board(8).grid()    # поле гри
        self.players = [1, -1]   # можливі значення для гравців
        self.player = 1
        self.add_point(4, 4, 1)  # додаємо початкові точки в центр поля
        self.add_point(3, 3, 1)
        self.add_point(3, 4, -1)
        self.add_point(4, 3, -1)
        self.play = True
        self.minimax = MiniMaxWithAlphaBeta(self)
        self.p1 = 0
        self.p2 = 0

    def add_point(self, x, y, n):   # додаємо 1 або -1 на поле
        self.board[y][x] = n
        return self.board

    def cells(self, player):
        valid_cell = []
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if self.board[x][y] != 0:
                    continue
                dirs = self.directions(x, y)

                for d in dirs:
                    Dx, Dy = d
                    checkCell = self.board[Dx][Dy]
                    if checkCell == 0 or checkCell == player:
                        continue
                    elif (x, y) in valid_cell:
                        continue
                    valid_cell.append((x, y))
        return valid_cell

    def moves(self, player):
        cells = self.cells(player)
        moves = []
        for cell in cells:
            x, y = cell
            if cell in moves:
                continue
            tiles = self.tiles(x, y, player)
            if len(tiles) > 0:
                moves.append(cell)
        return moves

    def print_grid(self):   # поле гри
        print()
        print('-----------------------------------')
        print('  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |')
        for i in range(len(self.board)):
            print(i, end=' | ')
            for j in range(len(self.board[i])):
                print(self.board[i][j], end=' | ')
            print()
        print('-----------------------------------')
        print()

    def tiles(self, x, y, player):
        cells = self.directions(x, y)   # сусідні клітинки для заданої
        if len(cells) == 0:
            return []
        swappable_tiles = []
        for cell in cells:
            x_, y_ = cell
            Dx, Dy = x_ - x, y_ - y
            current_line = []
            RUN = True
            while RUN:
                if self.board[x_][y_] == player * -1:
                    current_line.append((x_, y_))     # додаємо до списку перевіреної лінії фішки гравця
                elif self.board[x_][y_] == player:
                    RUN = False
                elif self.board[x_][y_] == 0:   # якщо натрапляємо на 0, то видаляємо елементи та зупиняємо цикл
                    current_line.clear()
                    RUN = False
                x_ += Dx
                y_ += Dy

                if 0 > x_ or 7 < x_ or 0 > y_ or 7 < y_:
                    current_line.clear()
                    RUN = False

            if len(current_line) > 0:
                swappable_tiles.extend(current_line)    # додаємо всі фішки, які потрібно перевернути
        return swappable_tiles

    def calculate_score(self, player):  # рахунок
        score = 0
        for row in self.board:
            for col in row:
                if col == player:   # якщо число в клітинці таблиці рівне номеру гравця, то йому плюсується бал
                    score += 1
        return score

    @staticmethod
    def directions(x, y):  # повертає сусідні клітинки до заданої за (x, y) координатами
        valid_dirs = []
        if x != 0:
            valid_dirs.append((x - 1, y))
            if y != 0:
                valid_dirs.append((x - 1, y - 1))
            if y != 7:
                valid_dirs.append((x - 1, y + 1))
        if x != 7:
            valid_dirs.append((x + 1, y))
            if y != 0:
                valid_dirs.append((x + 1, y - 1))
            if y != 7:
                valid_dirs.append((x + 1, y + 1))
        if y != 0:
            valid_dirs.append((x, y - 1))
        if y != 7:
            valid_dirs.append((x, y + 1))
        return valid_dirs

    def game(self):     # сама гра гри
        two_computers = int(input('Two computers(0) or player vs computer(1)'))
        while self.play:
            self.print_grid()
            if self.player == 1:
                if two_computers == 1:
                    x = int(input('X: '))
                    y = int(input('Y: '))
                    moves = self.moves(self.player)
                    if not moves:
                        pass
                    else:
                        if (y, x) in moves:
                            self.add_point(x, y, self.player)
                            swap_tiles = self.tiles(y, x, self.player)
                            for tile in swap_tiles:
                                self.board[tile[0]][tile[1]] *= -1
                            self.player *= -1
                elif two_computers == 0:
                    if not self.moves(self.player):
                        self.play = False
                        break
                    cell, score = self.minimax.minimax(self.board, 5, -64, 64,
                                                       self.player)  # вибираємо хід комп'ютера за мінімаксом
                    self.add_point(cell[1], cell[0], self.player)
                    swap_tiles = self.tiles(cell[0], cell[1], self.player)
                    for tile in swap_tiles:
                        self.board[tile[0]][tile[1]] *= -1
                    self.player *= -1
            else:
                if not self.moves(self.player):
                    self.play = False
                    break
                cell, score = self.minimax.minimax(self.board, 5, -64, 64, self.player)     # вибираємо хід комп'ютера за мінімаксом
                self.add_point(cell[1], cell[0], self.player)
                swap_tiles = self.tiles(cell[0],cell[1], self.player)
                for tile in swap_tiles:
                    self.board[tile[0]][tile[1]] *= -1
                self.player *= -1
            self.p1 = self.calculate_score(1)
            self.p2 = self.calculate_score(-1)
            if two_computers== 1:
                print(f'Player: {self.p1}')
                print(f"Computer: {self.p2}")
            else:
                print(f'Computer 1: {self.p1}')
                print(f"Computer 2: {self.p2}")
            if not self.moves(self.player):  # якщо немає доступних ходів, то зупиняємо гру
                self.play = False
                break






