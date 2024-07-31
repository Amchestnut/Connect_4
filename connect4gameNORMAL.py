import pygame
import sys
import numpy as np
from mcts import MCTSAgent
from minimax_final import MINIMAXAgentBot

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
WOOD_COLOR = (153, 102, 51)  # Wood-like color
BRIGHT_SKY_BLUE = (135, 206, 250)  # Bright sky blue color
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 5)
score_red = 0
score_yellow = 0

# Function to create the game board
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

# Function to drop a token into the board
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

# Function to draw the game board
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, WOOD_COLOR, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BRIGHT_SKY_BLUE, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    pygame.display.update()

# Function to handle player input and moves
def player_input():
    posx = pygame.mouse.get_pos()[0]
    col = int(posx // SQUARE_SIZE)
    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_token(board, row, col, 1)
        if winning_move(board, 1):
            return True
    return False

# Function to handle MCTS moves
def mcts_move_red():
    col = mcts_agent_red.monte_carlo_tree_search(board)
    row = get_next_open_row(board, col)
    drop_token(board, row, col, 1)
    if winning_move(board, 1):
        return True
    return False

# Function to handle MCTS moves
def mcts_move_yellow():
    col = mcts_agent_yellow.monte_carlo_tree_search(board)
    row = get_next_open_row(board, col)
    drop_token(board, row, col, 2)
    if winning_move(board, 2):
        return True
    return False

# NEW minimax function, that handle moves either first or second
def minmax_move_new():
    col = minimax_agent_new.bestMove(board) 
    row = get_next_open_row(board, col)
    drop_token(board, row, col, 2)
    if winning_move(board, 2):
        return True
    return False

# Function to handle gameOver
def game_over_logic():
    pygame.time.wait(300)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Check for Enter key
                    waiting = False
                    pygame.quit()
                    
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
# Main game loop
board = create_board()
game_over = False
turn = 0
pygame.init()
square_size = SQUARE_SIZE
width = COLUMN_COUNT * square_size
height = (ROW_COUNT + 1) * square_size
size = (width, height)
screen = pygame.display.set_mode(size)
screen.fill(BRIGHT_SKY_BLUE)  # Set background color
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)

# MCTS agent
mcts_agent_red = MCTSAgent(4000, ROW_COUNT, COLUMN_COUNT,1)
mcts_agent_yellow = MCTSAgent(4000, ROW_COUNT, COLUMN_COUNT,2)

# New minimax agent
minimax_agent_new = MINIMAXAgentBot(5,ROW_COUNT,COLUMN_COUNT,2)

score_font = pygame.font.SysFont("monospace", 30)
score_label = score_font.render(f"Player 1: {score_red}  Player 2: {score_yellow}", 1, (0, 0, 0))
screen.blit(score_label, (10, 10))
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass

    if mcts_move_red():
            label = myfont.render("Player 1 wins!", 1, YELLOW)
            screen.blit(label, (40, 10))
            update_scores(1)  # Update scores if Player 2 wins, valjda 1
            game_over = True

    draw_board(board)

    # Display scores
    pygame.display.update()

    if not game_over:
        
        if minmax_move_new():
            label = myfont.render("Player 2 wins!", 1, RED)
            screen.blit(label, (40, 10))
            update_scores(2)  # Update scores if Player 1 wins
            game_over = True

        draw_board(board)

        pygame.display.update()

    if game_over:
        pygame.time.wait(3000)  # Wait for a few seconds before resetting the game
        board = create_board()  # Reset the board
        screen.fill(BRIGHT_SKY_BLUE)
        score_label = score_font.render(f"Player 1: {score_red}  Player 2: {score_yellow}", 1, (0, 0, 0))
        screen.blit(score_label, (2, 2))
        draw_board(board)
        pygame.display.update()
        game_over = False

pygame.quit()  # Quit pygame once the game is over
