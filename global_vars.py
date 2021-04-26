import numpy as np
from graphic_ui.gui_consts import COLORS

def init():
    # ========== Global variables for Game Logic =============
    # True if there is a winner, False if it is a tie
    global hasWinner
    hasWinner = False
    global winner_name
    winner_name = None

    # Player information
    global player_name_1
    player_name_1 = "Player 1"
    global player_name_2
    player_name_2 = "Player 2"

    global player_score_1
    player_score_1 = 0
    global player_score_2
    player_score_2 = 0
    
    # first == 0 -> Change and current = 0 ("O")
    # first == 1 -> Change and current = 1 ("X")
    # first == 2 -> Only "O"
    # first == 3 -> Only "X"
    global first_value
    first_value = 3

    # Level for singleplayer
    global level
    level = 1
    global level_p1
    level_p1 = 1
    global level_p2
    level_p2 = 1

    global colors
    colors = COLORS[:2]

    global board
    board = np.zeros((3, 3))