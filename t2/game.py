from display import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1100, 800))
        pygame.display.set_caption("Reversi")
        self.player1 = 1    # гравці
        self.player2 = -1
        self.currentPlayer = 1
        self.time = 0
        self.grid = WorkWithGrid(8, 8, 80, self)    # об'єкт для роботи із механікою гри
        self.comp_player = MiniMax(self.grid)   # алгоритм
        self.RUN = True
        self.game_over = False

    def run(self):  # запуск гри
        while self.RUN == True:
            self.input()
            self.update()
            self.draw()

    def input(self):    # запуск механіки гри
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # вихід із гри
                self.RUN = False

            # для комп'ютера проти гравця
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:   # при натиску на ліву кнопку, ми можемо зробити хід
                    if self.currentPlayer == 1 and not self.game_over:
                        x, y = pygame.mouse.get_pos()
                        x, y = (x - 80) // 80, (y - 80) // 80
                        valid_cells = self.grid.find_avail_moves(self.grid.logic, self.currentPlayer)   #
                        if not valid_cells:
                            pass
                        else:
                            if (y, x) in valid_cells:   #
                                self.grid.add_token(self.grid.logic, self.currentPlayer, y, x)
                                swappable_tiles = self.grid.swappable_tiles(y, x, self.grid.logic, self.currentPlayer)
                                for tile in swappable_tiles:
                                    self.grid.anim_transitions(tile, self.currentPlayer)
                                    self.grid.logic[tile[0]][tile[1]] *= -1
                                self.currentPlayer *= -1
                                self.time = pygame.time.get_ticks()
                    if self.game_over:
                        x, y = pygame.mouse.get_pos()
                        if 320 <= x <= 480 and 400 <= y <= 480:
                            self.grid.new_game()
                            self.game_over = False


    def update(self):
        if self.currentPlayer == -1:    # хід комп'ютера
            new_time = pygame.time.get_ticks()
            if new_time - self.time >= 1000:
                if not self.grid.find_avail_moves(self.grid.logic, self.currentPlayer):
                    self.game_over = True
                    return
                cell, score = self.comp_player.comp_hard(self.grid.logic, 5, -64, 64, -1)
                self.grid.add_token(self.grid.logic, self.currentPlayer, cell[0], cell[1])
                swappable_tiles = self.grid.swappable_tiles(cell[0],cell[1], self.grid.logic, self.currentPlayer)
                for tile in swappable_tiles:
                    self.grid.anim_transitions(tile, self.currentPlayer)
                    self.grid.logic[tile[0]][tile[1]] *= -1
                self.currentPlayer *= -1
        self.grid.player1Score = self.grid.calculate_score(self.player1)    # підрахунок фішок гравців
        self.grid.player2Score = self.grid.calculate_score(self.player2)    #
        if not self.grid.find_avail_moves(self.grid.logic, self.currentPlayer):  # якщо немає доступних ходів, то зупиняємо гру
            self.game_over = True
            return

    def draw(self):    
        self.screen.fill((0, 0, 0))
        self.grid.draw_grid(self.screen)
        pygame.display.update()


if __name__ == '__main__':  # запуск гри
    game = Game()
    game.run()
    pygame.quit()
