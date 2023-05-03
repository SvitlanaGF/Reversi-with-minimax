import copy


def score(grid):
    score = 0
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            score -= col
    return score


class MiniMaxWithAlphaBeta:
    def __init__(self, reversi):
        self.reversi = reversi

    def minimax(self, new_grid, depth, alpha, beta, player):
        grid = copy.deepcopy(new_grid)
        moves = self.reversi.moves(player)
        if depth == 0 or len(moves) == 0:
            return None, score(new_grid)
        if player == -1:
            bestMove = None
            b_score = -64
            for move in moves:
                x = move[0]
                y = move[1]
                tiles = self.reversi.tiles(x, y, player)
                grid[x][y] = player
                for tile in tiles:
                    grid[tile[0]][tile[1]] = player
                b_move, val = self.minimax(grid, depth-1, alpha, beta, player * -1)
                if val > b_score:
                    b_score = val
                    bestMove = move
                alpha = max(alpha, b_score)
                if beta <= alpha:
                    break
                grid = copy.deepcopy(new_grid)
            return bestMove, b_score
        elif player == 1:
            bestMove = None
            b_score = 64
            for move in moves:
                x = move[0]
                y = move[1]
                tiles = self.reversi.tiles(x, y, player)
                grid[x][y] = player
                for tile in tiles:
                    grid[tile[0]][tile[1]] = player
                b_move, val = self.minimax(grid, depth-1, alpha, beta, player * -1)
                if val < b_score:
                    b_score = val
                    bestMove = move
                beta = min(beta, b_score)
                if beta <= alpha:
                    break
                grid = copy.deepcopy(new_grid)
            return bestMove, b_score
