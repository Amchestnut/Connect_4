import unittest
import numpy as np
from Utils_and_visual_look.Utility_functions import *
from Models.Minimax import MINIMAXAgent
from Models.Monte_carlo_tree_search import MCTSAgent

class TestConnect4(unittest.TestCase):

    def setUp(self):
        self.board = create_board()
        self.minimax = MINIMAXAgent(5, ROW_COUNT, COLUMN_COUNT, player=1)
        self.mcts = MCTSAgent(100, ROW_COUNT, COLUMN_COUNT, player=2)

    def test_winning_move(self):
        # Horizontal win
        self.board[0, 0] = self.board[0, 1] = self.board[0, 2] = self.board[0, 3] = 1  # Add the fourth token
        self.assertTrue(winning_move(self.board, 1))
        # No win
        self.assertFalse(winning_move(self.board, 2))

    def test_is_valid_location(self):
        self.assertTrue(is_valid_location(self.board, 0))
        self.board[:, 0] = 1  # Fill column
        self.assertFalse(is_valid_location(self.board, 0))

    def test_get_next_open_row(self):
        self.assertEqual(get_next_open_row(self.board, 0), 0)
        self.board[0, 0] = 1
        self.assertEqual(get_next_open_row(self.board, 0), 1)

    def test_minimax_ai_move(self):
        self.board[0, 0] = self.board[0, 1] = self.board[0, 2] = 1  # Set up AI to win
        best_move = self.minimax.bestMove(self.board)
        self.assertEqual(best_move, 3)  # Minimax should block the win

    def test_mcts_ai_move(self):
        col = self.mcts.monte_carlo_tree_search(self.board)
        self.assertTrue(is_valid_location(self.board, col))  # MCTS should make a valid move


if __name__ == '__main__':
    unittest.main()
