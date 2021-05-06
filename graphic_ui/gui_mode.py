import pygame
import pygame_menu
import sys
from graphic_ui.gui_consts import *
from graphic_ui.draw_text import *
import global_vars as gv
import game_logic as gl
from console.singleplayer import random_move, medium_move, minimax
import numpy as np

# ========= PyGame Initialization ==========
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

bg_image = pygame.image.load("images/bg_image.jpg")

# Settings for buttons and text location
replay_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
back_button =   pygame.Rect(WIDTH // 1.11 - BACK_BUTTON_WIDTH // 2, HEIGHT // 20 - BACK_BUTTON_HEIGHT // 2, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT)
reset_button =  pygame.Rect(WIDTH // 10 - BACK_BUTTON_WIDTH // 2, HEIGHT // 20 - BACK_BUTTON_HEIGHT // 2, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT)

winner_text =   pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 3 - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
scores_text =   pygame.Rect(WIDTH // 2, HEIGHT - SCORE_MARGIN - SCORE_DIST_HEIGHT // 2, SCORE_DIST_WIDTH, SCORE_DIST_HEIGHT)

def draw_window(first_player):
    screen.blit(bg_image, (0, 0))
    draw_board()
    draw_symbols()
    draw_scores(screen, scores_text, first_player)
    draw_button("Back", screen, back_button)
    draw_button("New", screen, reset_button)

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
                pygame.draw.line(screen, gv.colors[0], (column + SQUARE_MARGIN, row + SQUARE_SIZE - SQUARE_MARGIN), (column + SQUARE_SIZE - SQUARE_MARGIN, row + SQUARE_MARGIN), CROSS_WIDTH)
                # Line from top left to bottem right corner
                pygame.draw.line(screen, gv.colors[0], (column + SQUARE_MARGIN, row + SQUARE_MARGIN), (column + SQUARE_SIZE - SQUARE_MARGIN, row + SQUARE_SIZE - SQUARE_MARGIN), CROSS_WIDTH)
            elif gv.board[i][j] == 2:
                # Draw an 'O'
                pygame.draw.circle(screen, gv.colors[1], (column + SQUARE_SIZE // 2, row + SQUARE_SIZE // 2 ), CIRLE_RADIUS, CIRCLE_WIDTH)

def solved(line, symbol):
    return np.all(line == symbol)

def draw_winner_line(board):
    size = board.shape[0]
    # Check all rows
    for i in range(size):
        winner_color = gv.colors[0] if solved(board[i], 1) else gv.colors[1] if solved(board[i], 2) else None
        if winner_color:
            y_pos = MARGIN + i * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.line(screen, winner_color, (MARGIN, y_pos), (MARGIN + size * SQUARE_SIZE, y_pos), CROSS_WIDTH)
            return
    
    # Check all columns
    for i in range(size):
        winner_color = gv.colors[0] if solved(np.transpose(board)[i], 1) else gv.colors[1] if solved(np.transpose(board)[i], 2) else None
        if winner_color:
            x_pos = MARGIN + i * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.line(screen, winner_color, (x_pos, MARGIN), (x_pos, MARGIN + size * SQUARE_SIZE), CROSS_WIDTH)
            return

    # Check diagonals
    line = np.array([board[0][0], board[1][1], board[2][2]])
    winner_color = gv.colors[0] if solved(line, 1) else gv.colors[1] if solved(line, 2) else None
    if winner_color:
        pygame.draw.line(screen, winner_color, (MARGIN, MARGIN), (MARGIN + size * SQUARE_SIZE, MARGIN + size * SQUARE_SIZE), CROSS_WIDTH)
    
    line = np.array([board[2][0], board[1][1], board[0][2]])
    winner_color = gv.colors[0] if solved(line, 1) else gv.colors[1] if solved(line, 2) else None
    if winner_color:
        pygame.draw.line(screen, winner_color, (MARGIN, MARGIN + size * SQUARE_SIZE), (MARGIN + size * SQUARE_SIZE, MARGIN), CROSS_WIDTH)

def move_is_valid(x_pos, y_pos):
    return (0 <= x_pos < gv.board.shape[0] and 
            0 <= y_pos < gv.board.shape[0] and 
            (x_pos * 3 + y_pos) + 1 in gl.get_free_moves(gv.board))

def reset_scores():
    gv.player_score_1 = 0
    gv.player_score_2 = 0

def make_human_move_gui(event, gm_over, current_sym):
        x_pos = event.pos[0]
        y_pos = event.pos[1]

        # Calculate the corresponding board position in [(0, 0), ..., (2, 2)]
        # board positions containing -1 or 3 are invalid and outside of the board
        board_x_pos = (y_pos - MARGIN) // SQUARE_SIZE
        board_y_pos = (x_pos - MARGIN) // SQUARE_SIZE

        symbol = "X" if current_sym else "O"
        if move_is_valid(board_x_pos, board_y_pos):
            gl.add_symbol(symbol, (board_x_pos * 3 + board_y_pos) + 1)
            
            # Change player
            current_sym = 1 - current_sym
            return gl.check_game_over(gv.board), current_sym

def make_comp_move_gui(current_sym, level):
    # own symbol
    symbol = "X" if current_sym else "O"
    # Easy
    if level == 1:
       pos = random_move()
    # Medium
    elif level == 2:
        # Computer blocks and choses corners > middle > edge
        pos = medium_move()
    # Hard (Undefeatable)
    elif level == 3:
        # First two moves are chosen randomly so the human has a chance to win
        if len(gl.get_free_moves(gv.board)) in [8, 9]:
            pos = random_move()
        else:
            board_copy = np.copy(gv.board)
            pos = minimax(board_copy, symbol, symbol)['pos']

    gl.add_symbol(symbol, pos)

    current_sym = 1 - current_sym
    return gl.check_game_over(gv.board), current_sym

def play_gui(single_mode):
    # Disable the main menu loop
    from graphic_ui.menus.main_menu import menu
    global menu
    menu.disable()
    menu.full_reset()

    # Reset Game Logic
    gl.reset_game()
    gm_over = False
    pause = True
    clicked = False

    # first == 0 -> Change and current = 0 ("O")
    # first == 1 -> Change and current = 1 ("X")
    # first == 2 -> Only "O"
    # first == 3 -> Only "X"
    # Change the value of first from (0 <-> 1) if necessary
    gv.first_value = 1 - gv.first_value if gv.first_value in [0, 1] else gv.first_value

    # Determine current symbol
    current_sym = 0 if gv.first_value == 2 else 1 if gv.first_value == 3 else gv.first_value

    # Game Loop for GUI
    while True:
        clock.tick(FPS)
        
        # Computer moves
        if single_mode and not gm_over:
            # PC vs PC first player
            if current_sym == 1 and gv.level == 4: # "X"
                gm_over, current_sym = make_comp_move_gui(current_sym, gv.level_p1)
            # PC vs PC second player
            elif current_sym == 0 and gv.level == 4: # "O"
                # Computer plays at level p2 vs other computer
                gm_over, current_sym = make_comp_move_gui(current_sym, gv.level_p2)     
            # Human vs PC: Computer plays at level gv.level
            elif current_sym == 0: # "O"
                gm_over, current_sym = make_comp_move_gui(current_sym, gv.level)
                pygame.display.update()
                pygame.time.wait(400)
                if gv.sound_on:
                    pygame.mixer.Sound.play(DRAW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    reset_scores()
                    menu.enable()
                    return

            # User moves in single ("X") or multiplayer
            if single_mode and current_sym == 1 or not single_mode:
                # Check for a mouse click (down AND up again)
                if event.type == pygame.MOUSEBUTTONDOWN and not gm_over:
                    clicked = True
                if event.type == pygame.MOUSEBUTTONUP and clicked:
                    clicked = False
                    result = make_human_move_gui(event, gm_over, current_sym)
                    if result:
                        if gv.sound_on:
                            pygame.mixer.Sound.play(DRAW)
                        gm_over, current_sym = result            

        draw_window(current_sym)

        if gm_over:
            draw_winner_line(gv.board)
            
            # Pause after the game is over
            if pause:
                pygame.display.update()
                pygame.time.wait(400)
                pause = False

            draw_winner_name(gv.winner_name + " wins!" if gv.hasWinner else "Tie!", screen, winner_text)
            draw_button("Play Again", screen, replay_button)
            if gv.level == 4 or check_clicked(replay_button):
                if gv.level != 4 and gv.sound_on:
                    pygame.mixer.Sound.play(CLICK)
                play_gui(single_mode)

        if check_clicked(back_button):
            reset_scores()
            if gv.sound_on:
                pygame.mixer.Sound.play(CLICK)
            menu.enable()
            return
        
        if check_clicked(reset_button):
            gl.reset_game()
            if gv.sound_on:
                pygame.mixer.Sound.play(CLICK)
                pygame.display.update()
                pygame.time.wait(500)            

        pygame.display.update()