import sys
import pygame
import numpy as np

from Utils_and_visual_look.Utility_functions import *
from Utils_and_visual_look.Visual_look import *
from Models.Monte_carlo_tree_search import MCTSAgent
from Models.Minimax import MINIMAXAgent
from Utils_and_visual_look.Constants import *

def get_player_type(player_number):
    print(f"Select Player {player_number} type:")
    print("1. Human")
    print("2. Minimax AI")
    print("3. MCTS AI")
    choice = input("Enter 1, 2, or 3: ")
    while choice not in ['1', '2', '3']:
        choice = input("Invalid input. Enter 1, 2, or 3: ")
    if choice == '1':
        return 'human'
    elif choice == '2':
        return 'minimax'
    elif choice == '3':
        return 'mcts'

def main():
    # Get player types
    player1_type = get_player_type(1)
    player2_type = get_player_type(2)

    # Initialize game variables
    board = create_board()
    game_over = False
    turn = 0

    # Initial game look settings
    pygame.init()
    screen = pygame.display.set_mode(size)
    screen.fill(BRIGHT_SKY_BLUE)
    draw_board(board, screen)
    pygame.display.update()
    myfont = pygame.font.SysFont("monospace", 75)

    # Initialize AI agents
    minimax_agent_player1 = None
    mcts_agent_player1 = None
    minimax_agent_player2 = None
    mcts_agent_player2 = None

    if player1_type == 'minimax':
        minimax_agent_player1 = MINIMAXAgent(5, ROW_COUNT, COLUMN_COUNT, 1)
    elif player1_type == 'mcts':
        mcts_agent_player1 = MCTSAgent(4000, ROW_COUNT, COLUMN_COUNT, 1)

    if player2_type == 'minimax':
        minimax_agent_player2 = MINIMAXAgent(5, ROW_COUNT, COLUMN_COUNT, 2)
    elif player2_type == 'mcts':
        mcts_agent_player2 = MCTSAgent(4000, ROW_COUNT, COLUMN_COUNT, 2)


    # Handle Human move
    def human_move(token):
        posx = pygame.mouse.get_pos()[0]
        col = int(posx // SQUARE_SIZE)
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_token(board, row, col, token)
            if winning_move(board, token):
                return True
        return False

    # Handle Minimax move
    def minimax_move(token):
        if token == 1:
            col = minimax_agent_player1.bestMove(board)
        else:
            col = minimax_agent_player2.bestMove(board)
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_token(board, row, col, token)
            if winning_move(board, token):
                return True
        return False

    # Handle MTCS move
    def mcts_move(token):
        if token == 1:
            col = mcts_agent_player1.monte_carlo_tree_search(board)
        else:
            col = mcts_agent_player2.monte_carlo_tree_search(board)
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_token(board, row, col, token)
            if winning_move(board, token):
                return True
        return False

    # Main game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if ((turn == 0 and player1_type == 'human') or (turn == 1 and player2_type == 'human')):
                    token = 1 if turn == 0 else 2
                    if human_move(token):
                        label = myfont.render(f"Player {token} wins!", 1, RED if token == 1 else YELLOW)
                        screen.blit(label, (40, 10))
                        update_scores(token)
                        game_over = True

                    draw_board(board, screen)
                    draw_legend(player1_type, player2_type, screen)
                    pygame.display.update()
                    turn = (turn + 1) % 2

        if not game_over:
            if turn == 0 and player1_type != 'human':
                token = 1
                if player1_type == 'minimax':
                    if minimax_move(token):
                        label = myfont.render("Player 1 wins!", 1, RED)
                        screen.blit(label, (40, 10))
                        update_scores(1)
                        game_over = True
                elif player1_type == 'mcts':
                    if mcts_move(token):
                        label = myfont.render("Player 1 wins!", 1, RED)
                        screen.blit(label, (40, 10))
                        update_scores(1)
                        game_over = True
                draw_board(board, screen)
                draw_legend(player1_type, player2_type, screen)
                pygame.display.update()
                turn = (turn + 1) % 2

            elif turn == 1 and player2_type != 'human':
                token = 2
                if player2_type == 'minimax':
                    if minimax_move(token):
                        label = myfont.render("Player 2 wins!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        update_scores(2)
                        game_over = True
                elif player2_type == 'mcts':
                    if mcts_move(token):
                        label = myfont.render("Player 2 wins!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        update_scores(2)
                        game_over = True
                draw_board(board, screen)
                draw_legend(player1_type, player2_type, screen)
                pygame.display.update()
                turn = (turn + 1) % 2

        # Check for draw
        if check_draw(board):
            label = myfont.render("It's a draw!", 1, (255, 255, 255))
            screen.blit(label, (40, 10))
            game_over = True

        if game_over:
            pygame.time.wait(3000)

            # Reset the game
            board = create_board()
            screen.fill(BRIGHT_SKY_BLUE)
            draw_board(board, screen)
            draw_legend(player1_type, player2_type, screen)
            pygame.display.update()
            game_over = False
            turn = 0  # Reset turn if needed

    pygame.quit()

if __name__ == "__main__":
    main()
