from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'HIDE'
import pygame
pygame.init()
import pygame_menu
import sys
from gui_consts import *
import global_vars as gv
import game_logic as gl
from draw_text import *
import numpy as np

# ========= PyGame Initialization ==========
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

# Settings for buttons and text location
replay_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
back_button =   pygame.Rect(WIDTH // 1.05 - BUTTON_WIDTH // 2, HEIGHT // 20 - BUTTON_HEIGHT // 2, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT)

winner_text =   pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 3 - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
scores_text =   pygame.Rect(WIDTH // 2 - SCORE_WIDTH // 2, HEIGHT - SCORE_MARGIN - SCORE_HEIGHT // 2, SCORE_WIDTH, SCORE_HEIGHT)

def draw_window(first_player):
    screen.fill(BG_COLOR)
    draw_board()
    draw_symbols()
    draw_scores(screen, scores_text, first_player)
    draw_button("Back", screen, back_button)

def draw_board():
    size = gv.board.shape[0]
    for i in range(1, size):
        pygame.draw.line(screen, BOARD_COLOR, (i * SQUARE_SIZE + MARGIN, MARGIN), (i * SQUARE_SIZE + MARGIN, size * SQUARE_SIZE + MARGIN), LINE_WIDTH)
        pygame.draw.line(screen, BOARD_COLOR, (MARGIN, i * SQUARE_SIZE + MARGIN), (size * SQUARE_SIZE + MARGIN, i * SQUARE_SIZE + MARGIN), LINE_WIDTH)

def draw_symbols():
    size = gv.board.shape[0]
    for i in range(size):
        for j in range(size):
            column = j * SQUARE_SIZE + MARGIN
            row = i * SQUARE_SIZE + MARGIN
            if gv.board[i][j] == 1:
                # Draw an 'X'
                # Line from bottom left to top right corner
                pygame.draw.line(screen, CROSS_COLOR, (column + SQUARE_MARGIN, row + SQUARE_SIZE - SQUARE_MARGIN), (column + SQUARE_SIZE - SQUARE_MARGIN, row + SQUARE_MARGIN), CROSS_WIDTH)
                # Line from top left to bottem right corner
                pygame.draw.line(screen, CROSS_COLOR, (column + SQUARE_MARGIN, row + SQUARE_MARGIN), (column + SQUARE_SIZE - SQUARE_MARGIN, row + SQUARE_SIZE - SQUARE_MARGIN), CROSS_WIDTH)
            elif gv.board[i][j] == 2:
                # Draw an 'O'
                pygame.draw.circle(screen, CIRCLE_COLOR, (column + SQUARE_SIZE // 2, row + SQUARE_SIZE // 2 ), CIRLE_RADIUS, CIRCLE_WIDTH)

def solved(line, symbol):
    return np.all(line == symbol)

def draw_winner_line(board):
    size = board.shape[0]
    # Check all rows
    for i in range(size):
        winner_color = CROSS_COLOR if solved(board[i], 1) else CIRCLE_COLOR if solved(board[i], 2) else None
        if winner_color:
            y_pos = MARGIN + i * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.line(screen, winner_color, (MARGIN, y_pos), (MARGIN + size * SQUARE_SIZE, y_pos), CROSS_WIDTH)
            return
    
    # Check all columns
    for i in range(size):
        winner_color = CROSS_COLOR if solved(np.transpose(board)[i], 1) else CIRCLE_COLOR if solved(np.transpose(board)[i], 2) else None
        if winner_color:
            x_pos = MARGIN + i * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.line(screen, winner_color, (x_pos, MARGIN), (x_pos, MARGIN + size * SQUARE_SIZE), CROSS_WIDTH)
            return

    # Check diagonals
    line = np.array([board[0][0], board[1][1], board[2][2]])
    winner_color = CROSS_COLOR if solved(line, 1) else CIRCLE_COLOR if solved(line, 2) else None
    if winner_color:
        pygame.draw.line(screen, winner_color, (MARGIN, MARGIN), (MARGIN + size * SQUARE_SIZE, MARGIN + size * SQUARE_SIZE), CROSS_WIDTH)
    
    line = np.array([board[2][0], board[1][1], board[0][2]])
    winner_color = CROSS_COLOR if solved(line, 1) else CIRCLE_COLOR if solved(line, 2) else None
    if winner_color:
        pygame.draw.line(screen, winner_color, (MARGIN, MARGIN + size * SQUARE_SIZE), (MARGIN + size * SQUARE_SIZE, MARGIN), CROSS_WIDTH)

def move_is_valid(x_pos, y_pos):
    return (0 <= x_pos < gv.board.shape[0] and 
            0 <= y_pos < gv.board.shape[0] and 
            (x_pos * 3 + y_pos) + 1 in gl.get_free_moves(gv.board))

def reset_scores():
    gv.player_score_1 = 0
    gv.player_score_2 = 0

def play_gui(second_starts):
    # Disable the main menu loop
    from main_menu import menu
    global menu
    menu.disable()
    menu.full_reset()

    # Reset Game Logic
    gl.reset_game()
    gm_over = False
    first_player = not second_starts
    clicked = False
    pause = True

    # Game Loop for GUI
    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    reset_scores()
                    menu.enable()
                    return

            # Check for a mouse click (down AND up again)
            if event.type == pygame.MOUSEBUTTONDOWN and not gm_over:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked:
                clicked = False
                x_pos = event.pos[0]
                y_pos = event.pos[1]

                # Calculate the corresponding board position in [(0, 0), ..., (2, 2)]
                # board positions containing -1 or 3 are invalid and outside of the board
                board_x_pos = (y_pos - MARGIN) // SQUARE_SIZE
                board_y_pos = (x_pos - MARGIN) // SQUARE_SIZE

                symbol = "X" if first_player else "O"
                if move_is_valid(board_x_pos, board_y_pos):
                    gl.add_symbol(symbol, (board_x_pos * 3 + board_y_pos) + 1)
                    
                    first_player = not first_player

                    gm_over = gl.check_game_over(gv.board)
                    
        draw_window(first_player)

        if gm_over:
            draw_winner_line(gv.board)
            
            # Pause after the game is over
            if pause:
                pygame.display.update()
                pygame.time.wait(500)
                pause = False

            draw_winner_name(gv.winner_name + " wins!" if gv.hasWinner else "Tie!", screen, winner_text)
            draw_button("Play Again", screen, replay_button)
            if check_clicked(replay_button):
                second_starts = not second_starts
                play_gui(second_starts)

        if check_clicked(back_button):
            reset_scores()
            menu.enable()
            return

        pygame.display.update()