import numpy as np
import random, math
from Utils_and_visual_look.Utility_functions import *

class MINIMAXAgent:
    WINDOW_LENGTH = 4
    EMPTY = 0

    def __init__(self, minimax_depth, ROW_COUNT, COLUMN_COUNT, player):
        self.minimax_depth = minimax_depth
        self.ROW_COUNT = ROW_COUNT
        self.COLUMN_COUNT = COLUMN_COUNT
        self.player = player  # So if player 1, player will be 1, if player = 2, player 2

    def get_next_open_row(self, board, col):
        for r in range(self.ROW_COUNT):
            if board[r][col] == 0:
                return r

    # Get all possible moves, so if there is 7 columns in which a token can be dropped into, it will return 7, if 6 then 6 etc.
    def get_possible_moves(self, board):
        return list({i for i in range(self.COLUMN_COUNT) for j in range(self.ROW_COUNT) if board[j][i] == 0})

    def is_terminal_node(self, board):
        # Check for win for either player
        if winning_move(board, self.player) or winning_move(board, 2 if self.player == 1 else 1):
            return True

        # Check if there are no more valid moves left (i.e., if the board is full)
        if all(board[self.ROW_COUNT - 1][c] != 0 for c in range(self.COLUMN_COUNT)):
            return True

        # If neither player has won and there are still moves left, it's not a terminal node
        return False

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = 2 if piece == 1 else 1  # Determinising the opponents piece, based on the current piece

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(self.EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(self.EMPTY) == 2:
            score += 2

        # If the opponent successed in connecting 3 tokens, punish my player with -4
        if window.count(opp_piece) == 3 and window.count(self.EMPTY) == 1:
            score -= 4

        return score

    def score_position(self, board, piece):
        score = 0

        # Score center column
        center_array = [int(i) for i in list(board[:, self.COLUMN_COUNT // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score Horizontal
        for r in range(self.ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.COLUMN_COUNT - 3):
                window = row_array[c:c + self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Score Vertical
        for c in range(self.COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.ROW_COUNT - 3):
                window = col_array[r:r + self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Score posiive sloped diagonal
        for r in range(self.ROW_COUNT - 3):
            for c in range(self.COLUMN_COUNT - 3):
                window = [board[r + i][c + i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(self.ROW_COUNT - 3):
            for c in range(self.COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_possible_moves(board)
        is_terminal = self.is_terminal_node(board)
        opp_piece = 2 if self.player == 1 else 1

        if depth == 0 or is_terminal:
            if is_terminal:  # We added here the check if it is a game win/lose move
                if winning_move(board, self.player):  # 1 is my player, 2 is opposite
                    return 1000
                elif winning_move(board, opp_piece):
                    return -2500
                else:
                    return 0
            else:
                return self.score_position(board, self.player)

        if maximizingPlayer:
            value = -math.inf
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                drop_token(b_copy, row, col, self.player)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)
                if new_score > value:
                    value = new_score
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value  # We return only the value (score), the actual best score for THE GIVEN MOVE (the initial 1 of the 7 moves possible)

        else:  # Minimizing player (opponent)
            value = math.inf
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                drop_token(b_copy, row, col, opp_piece)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)
                if new_score < value:
                    value = new_score
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value  # Return only the score

    def bestMove(self, board):
        best_score = -math.inf
        best_col = None
        for col in self.get_possible_moves(board):
            row = self.get_next_open_row(board, col)
            temp_board = board.copy()
            drop_token(temp_board, row, col, self.player)  # Drop the token 1 or 2, depending on the initialized player
            score = self.minimax(temp_board, self.minimax_depth, -math.inf, math.inf, False)
            if score > best_score:
                best_score = score
                best_col = col
        return best_col  # Return the best column
