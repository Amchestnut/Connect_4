import numpy as np

from Utils_and_visual_look.Constants import *



# Function to create the game board
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

# Function to drop a token in the selected column
def drop_token(board, row, col, token):
    board[row][col] = token

# Function to check if the selected column is valid for placing a token
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0  # If the bottom row in the selected column is empty, it's a valid move

# Function to get the next available row in a column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


# Function to check for a winning move
def winning_move(board, token):
    # Check horizontal locations for a win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == token and board[r][c + 1] == token and board[r][c + 2] == token and board[r][c + 3] == token:
                return True

    # Check vertical locations for a win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == token and board[r + 1][c] == token and board[r + 2][c] == token and board[r + 3][c] == token:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == token and board[r + 1][c + 1] == token and board[r + 2][c + 2] == token and board[r + 3][c + 3] == token:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == token and board[r - 1][c + 1] == token and board[r - 2][c + 2] == token and board[r - 3][c + 3] == token:
                return True


def print_board_matrix(board):
    for row in board[::-1]:  # Reverse the board to print it properly
        print(row)


def update_scores(winner):
    global score_red, score_yellow
    if winner == 1:
        score_red += 1
    elif winner == 2:
        score_yellow += 1


def check_draw(board):
    return not any(0 in row for row in board)