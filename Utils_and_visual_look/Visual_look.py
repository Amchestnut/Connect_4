import pygame
from Utils_and_visual_look.Constants import *

def draw_board(board, screen):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # Adjust rectangles and circles to account for the two extra rows
            pygame.draw.rect(screen, WOOD_COLOR, (c * SQUARE_SIZE, (r + 2) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BRIGHT_SKY_BLUE, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int((r + 2) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # Reverse row indexing for tokens to align correctly
            adjusted_row = ROW_COUNT - 1 - r
            if board[adjusted_row][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int((r + 2) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[adjusted_row][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int((r + 2) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    pygame.display.update()




# Function to draw the legend
def draw_legend(player1_type, player2_type, screen):
    legend_font = pygame.font.SysFont("monospace", 30)
    legend_label = legend_font.render(f"Player 1 ({player1_type.capitalize()}) vs Player 2 ({player2_type.capitalize()})", 1, (0, 0, 0))
    screen.blit(legend_label, (10, 10))  # Place legend at the very top


def draw_status(message, screen):
    status_font = pygame.font.SysFont("monospace", 50)
    status_label = status_font.render(message, 1, (255, 0, 0))
    screen.blit(status_label, (10, SQUARE_SIZE))  # Position below the legend