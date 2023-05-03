import pygame
import copy


class WorkWithGrid:
    tokens = dict()
    def __init__(self, row, column, size, main):
        self.game = main
        self.x = column
        self.y = row
        self.size = (size, size)
        self.white = self.work_with_img('imgs/white_token.png', self.size)
        self.black = self.work_with_img('imgs/black_token.png', self.size)
        self.bg = self.bgImgs()
        self.gridBG = self.createBGimg()
        self.logic = self.gen_grid(self.x, self.y)  # таблиця із ходами
        self.player1Score = 0
        self.player2Score = 0

        self.font = pygame.font.SysFont('Arial', 20, True, False)

    def new_game(self):
        self.tokens.clear()
        self.logic = self.gen_grid(self.y, self.x)

    def gen_grid(self, cols, rows):     # створює початкову розмітку
        grid = []
        for y in range(rows):
            line = []
            for x in range(cols):
                line.append(0)
            grid.append(line)
        self.add_token(grid, 1, 3, 3)
        self.add_token(grid, -1, 3, 4)
        self.add_token(grid, 1, 4, 4)
        self.add_token(grid, -1, 4, 3)
        return grid

    def bgImgs(self):   # фон гри
        alph = 'ABCDEFGH'
        sprite_sh = pygame.image.load('imgs/for_board_wood.jpg').convert_alpha()
        img_dict = dict()
        for i in range(3):
            for letter in alph:
                img_dict[letter+str(i)] = self.sprite_sheet(sprite_sh, alph.index(letter), i, self.size, (32, 32))
        return img_dict

    def calculate_score(self, player):  # рахунок
        score = 0
        for row in self.logic:
            for col in row:
                if col == player:   # якщо число в клітинці таблиці рівне номеру гравця, то йому плюсується бал
                    score += 1
        return score

    def draw_score(self, player, score):
        text_img = self.font.render(f'{player} : {score}', 1, 'White')  # вивід рахунку
        return text_img

    def endscreen(self):    # екран, який виводиться при закінченнi гри
        if self.game.game_over:
            end_screen = pygame.Surface((320, 320))
            end_text = self.font.render(f'{"Congratulations, You Won!!" if self.player1Score > self.player2Score else "Bad Luck, You Lost"}', 1, 'White')
            end_screen.blit(end_text,(0,0))
            new_game = pygame.draw.rect(end_screen, 'White', (80, 160, 160, 80))
            new_game_text = self.font.render('Play Again', 1, 'Black')
            end_screen.blit(new_game_text, (120, 190))
        return end_screen

    def draw_grid(self, window):
        window.blit(self.gridBG, (0, 0))
        window.blit(self.draw_score('White', self.player1Score), (900, 100))
        window.blit(self.draw_score('Black', self.player2Score), (900, 200))
        for token in self.tokens.values():
            token.draw(window)

        available_moves = self.find_avail_moves(self.logic, self.game.currentPlayer)
        if self.game.currentPlayer == 1:
            for move in available_moves:
                pygame.draw.rect(window, 'Green', (80 + (move[1]*80) + 30, 80 + (move[0] * 80)+30, 20, 20))
        if self.game.game_over:
            window.blit(self.endscreen(), (240, 240))

    def createBGimg(self):
        grid = [
            ['C0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'E0'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'E2']
        ]
        img = pygame.Surface((960, 960))
        for j, row in enumerate(grid):
            for i, im in enumerate(row):
                img.blit(self.bg[im], (i * self.size[0], j * self.size[1]))
        return img

    def find_valid_cells(self, grid, player):   # шукаємо доступні клітинки таблиці
        valid_cell_to_click = []
        for x, row in enumerate(grid):
            for y, col in enumerate(row):
                if grid[x][y] != 0:    # пропускаємо клітинки з 1 та -1
                    continue
                dirs = self.directions(x, y)    # список із координатів сусідніх клітинок для клітинки (х, у)

                for d in dirs:
                    Dx, Dy = d
                    checkCell = grid[Dx][Dy]

                    if checkCell == 0 or checkCell == player:   # пропускаємо нульові та ті, які мають значення поточного гравця клітинки
                        continue

                    if (x, y) in valid_cell_to_click:   # пропускаємо вже наявні клітинки у списку
                        continue
                    valid_cell_to_click.append((x, y))
        return valid_cell_to_click

    def add_token(self, grid, player, y, x):    # додавання фішок
        token_img = self.white if player == 1 else self.black   # додається біла фішка, якщо ходить гравець, чорна-- комп'ютер
        key = (y, x)
        self.tokens[key] = Token(player, y, x, token_img, self.game)    # у словник фігур додаємо фішку за заданими координатами
        grid[y][x] = self.tokens[key].player    # додаємо фішку на поле

    def find_avail_moves(self, grid, player):   # доступні ходи
        val_cells = self.find_valid_cells(grid, player)     # доступні клітинки
        playable_cells = []     # клітинки, по яких можна походити
        for cell in val_cells:
            x, y = cell
            if cell in playable_cells:  # пропускаємо клітинки, що вже є у списку
                continue
            swap_tiles = self.swappable_tiles(x, y, grid, player)   # перевертаємо

            if len(swap_tiles) > 0:
                playable_cells.append(cell)
        return playable_cells

    def swappable_tiles(self, x, y, grid, player):
        sur_cells = self.directions(x, y)   # сусідні клітинки для заданої
        if len(sur_cells) == 0:
            return []
        swappable_tiles = []
        for check_cell in sur_cells:
            check_x, check_y = check_cell
            Dx, Dy = check_x - x, check_y - y
            current_line = []
            RUN = True
            while RUN:
                if grid[check_x][check_y] == player * -1:
                    current_line.append((check_x, check_y))     # додаємо до списку перевіреної лінії фішки гравця
                elif grid[check_x][check_y] == player:
                    RUN = False
                    break
                elif grid[check_x][check_y] == 0:   # якщо натрапляємо на 0, то видаляємо елементи та зупиняємо цикл
                    current_line.clear()
                    RUN = False
                check_x += Dx
                check_y += Dy

                if 0 > check_x or 7 < check_x or 0 > check_y or 7 < check_y:
                    current_line.clear()
                    RUN = False

            if len(current_line) > 0:
                swappable_tiles.extend(current_line)    # додаємо всі фішки, які потрібно перевернути
        return swappable_tiles

    def anim_transitions(self, cell, player):
        if player == 1:
            self.tokens[(cell[0], cell[1])].trans(self.white)
        else:
            self.tokens[(cell[0], cell[1])].trans(self.black)
    @staticmethod
    def work_with_img(path, size):
        return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)

    @staticmethod
    def sprite_sheet(sheet, row, col, new_size, size):
        img = pygame.Surface((32, 32)).convert_alpha()
        img.blit(sheet, (0, 0), (row * size[0], col * size[1], size[0], size[1]))
        image = pygame.transform.scale(img, new_size)
        image.set_colorkey('Black')
        return image

    @staticmethod
    def directions(x, y, minX=0, minY=0, maxX=7, maxY=7):     # повертає сусідні клітинки до заданої за (x, y) координатами
        valid_dirs = []
        if x != minX:
            valid_dirs.append((x-1, y))
            if y != minY:
                valid_dirs.append((x-1, y-1))
            if y != maxY:
                valid_dirs.append((x-1, y+1))
        if x != maxX:
            valid_dirs.append((x + 1, y))
            if y != minY:
                valid_dirs.append((x + 1, y - 1))
            if y != maxY:
                valid_dirs.append((x + 1, y + 1))
        if y != minY:
            valid_dirs.append((x, y - 1))
        if y != maxY:
            valid_dirs.append((x, y + 1))
        return valid_dirs



class Token:    # фішки
    def __init__(self, player, gr_x, gr_y, img, main_obj):
        self.player = player
        self.gr_x = gr_x
        self.gr_y = gr_y
        self.position_x = 80 + (gr_y * 80)  #
        self.position_y = 80 + (gr_x * 80)  #
        self.img = img
        self.main_obj = main_obj

    def trans(self, token_img):
        self.img = token_img

    def draw(self, window):
        window.blit(self.img, (self.position_x, self.position_y))   #


class MiniMax:
    def __init__(self, grid_obj):
        self.grid = grid_obj

    def comp_hard(self, grid, depth, alpha, beta, player):
        new_grid = copy.deepcopy(grid)
        avail_moves = self.grid.find_avail_moves(new_grid, player)
        if depth == 0 or len(avail_moves) == 0:
            best_move, score = None, self.evaluate_board(grid, player)
            return best_move, score
        if player < 0:
            best_score = -64
            best_move = None
            for move in avail_moves:
                x, y = move
                swappable_tiles = self.grid.swappable_tiles(x, y, new_grid, player)
                new_grid[x][y] = player
                for tile in swappable_tiles:
                    new_grid[tile[0]][tile[1]] = player
                b_move, val = self.comp_hard(new_grid, depth-1, alpha, beta, player * -1)
                if val > best_score:
                    best_score = val
                    best_move = move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break

                new_grid = copy.deepcopy(grid)
            return best_move, best_score
        if player > 0:
            best_score = 64
            best_move = None
            for move in avail_moves:
                x, y = move
                swappable_tiles = self.grid.swappable_tiles(x, y, new_grid,player)
                new_grid[x][y] = player
                for tile in swappable_tiles:
                    new_grid[tile[0]][tile[1]] = player
                b_move, val = self.comp_hard(new_grid, depth-1, alpha, beta, player * -1)
                if val < best_score:
                    best_score = val
                    best_move = move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break

                new_grid = copy.deepcopy(grid)
            return best_move, best_score


    @staticmethod
    def evaluate_board(grid, player):
        score = 0
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                score -= col
        return score
