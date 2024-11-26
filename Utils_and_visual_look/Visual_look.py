import pygame
from Utils_and_visual_look.Constants import *

def draw_board(board, screen):
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

# Function to draw the legend
def draw_legend(player1_type, player2_type, screen):
    legend_font = pygame.font.SysFont("monospace", 30)
    legend_label = legend_font.render(f"Player 1 ({player1_type.capitalize()}) vs Player 2 ({player2_type.capitalize()})", 1, (0, 0, 0))
    screen.blit(legend_label, (10, 10))