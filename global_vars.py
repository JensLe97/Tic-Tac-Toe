import numpy as np

def init():
    # ========== Global variables for Game Logic =============
    # True if there is a winner, False if it is a tie
    global hasWinner
    hasWinner = False
    global winner_name
    winner_name = None

    # Player information
    global player_name_1
    player_name_1 = "J"
    global player_name_2
    player_name_2 = "L"

    global player_score_1
    player_score_1 = 0
    global player_score_2
    player_score_2 = 0

    global board
    board = np.zeros((3, 3))