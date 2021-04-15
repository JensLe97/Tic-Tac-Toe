import numpy as np
import random

# ========== Global variables for Game Logic =============
# True if there is a winner, False if it is a tie
hasWinner = False
winner_name = None

# Wheter or not players take turns at the beginning of each game
with_turns = False
# True if in this round the second player starts the game
second_starts = False

# Player information
player_name_1 = None
player_name_2 = None

player_score_1 = 0
player_score_2 = 0

board = np.zeros((3, 3))

# easy = 1 
# medium = 2
# hard = 3 
level = 0

# ======== Print Messages ===========
def print_welcome():
    print("========== TIC TAC TOE ==========")
    print()
    print("Welcome to the game of tic tac toe")
    print()
    

def print_rules():
    print("============ RULES ==============")
    print()
    print("In turns, players set 'X' or 'O' into the tiles of the board.")
    print("Whoever places three symbols in a row, a column or a diagonal wins.")
    print("Have Fun!")
    print()
    input("Press Enter to start...")
    
def print_ending():
    print("GAME OVER")
    if hasWinner:
        print(f"{winner_name} wins!")
    else:
        print("Tie!")
    print()
    print(f"Scores -- {player_name_1}: {player_score_1}, {player_name_2}: {player_score_2}")

# ====== User Input ========

def range_question(question, number):
    """Asks the user to select a number beween 1 and number and returns it as int"""
    while True:
        print()
        usr_in = input(question)
        try:
            n = int(usr_in)
            if n in range(1, number + 1):
                return n
            else:
                print("Please choose a valid game mode!")
        except ValueError:
            print("Please enter a valid number!")

def yes_no_question(question):
    """Asks the user a given yes/no questions and returns "y" or "n" """
    while True:
        print()
        again = input(question)

        if again in ["y", "n"]:
            return again
        else:
            print("Please choose 'y' for yes or 'n' for no!")

def name_question(question):
    """Asks the user for an arbitrary name and returns it"""
    while True:
        print()
        name = input(question)

        if name.strip() and name.strip()[0].isalpha():
            return name.strip()
        else:
            print("Please choose a non-empty name starting with a letter!")

# ========== Game Logic for single and multiplayer ===========

# ----------- Single Player Game ----------------

def start_singleplayer_game():
    """Core funcion of game implements the tic tac toe strategy (minmax algorithm)"""
    gm_over = False
    # Human player starts
    first_player = not second_starts
    reset_game()
    draw_board()

    while not gm_over:
        # Human's turn
        if first_player:
            gm_over = make_human_move(first_player)
        # Computer's turn
        else:
            gm_over = make_comp_move()
        
        first_player = not first_player

def make_comp_move():
    symbol = "O"
    # Easy
    if level == 1:
       pos = random.choice(get_free_moves())
    # Medium
    elif level == 2:
        # TODO: Change into a medium mode 
        # Computer blocks and choses corners > middle > edge
        pos = medium_move()
    # Hard (undefeatable)
    elif level == 3:
        if len(get_free_moves) == 9:
            pos = random.choice(get_free_moves())
        else:
            pos = minimax()

    add_symbol(symbol, pos)
    print()
    print(f"{player_name_2} has moved an 'O' to position {pos}")
    draw_board()
    return check_game_over(board)

def medium_move():
    free_moves = get_free_moves()

    # Check if any player is about to win with the next move: block it and take the win, respectively
    # 2 = "O" first: Winning has higher priority than blocking
    for sym in [2, 1]:
        for pos in free_moves:
            board_copy = np.copy(board)
            board_pos = pos - 1
            board_copy[board_pos // 3][board_pos % 3] = sym
            if check_game_over(board_copy, False):
                return pos
    
    # Choose a random corner
    corners = [i for i in free_moves if i in [1, 3, 7, 9]]
    if corners:
        return random.choice(corners)

    # Choose the middle
    if 5 in free_moves:
        return 5

    # Choose a random edge
    edges = [i for i in free_moves if i in [2, 4, 6, 8]]
    if edges:
        return random.choice(edges)      

def minimax():
    # TODO: Implements the minimax algorithm to maximize the computers chance of winning
    # Computer is player 2 = "O"
    my_sym = "O"
    other_sym = "X"
    return random.choice(get_free_moves())

# ------------ Multiplayer Game --------------

def start_multiplayer_game():
    """Core funcion of game for two players where each can decide where to place symbols"""
    # Reset Game logic
    gm_over = False
    # Wheter the first player ("X") starts the game or not
    first_player = not second_starts

    reset_game()
    draw_board()

    while not gm_over:
        gm_over = make_human_move(first_player)
        
        first_player = not first_player

# --------- Both Single and Multiplayer -------------

def get_free_moves():
    """ Returns a list of indices that can be chosen for a valid move"""
    # 2 np arrays containing the indices of row and column
    indices = np.where(board == 0)
    # zip into one list of the form [(i, j), (i, j), ...] 
    # with the empty fields (i, j)
    indices_2D = list(zip(indices[0], indices[1]))
    # retreive the position number from 2D to 1D (+1: like for human player (1-9))
    free = [(i * 3 + j) + 1 for i, j in indices_2D]
    return free

def make_human_move(first_player):
    """ Adds a player symbol to the board by asking for a position, then return wheter the game is over"""
    symbol = "X" if first_player else "O"
    valid_move = False
    while not valid_move:
        pos = range_question(f"{player_name_1 if first_player else player_name_2}, choose a position for '{symbol}': ", 9)
        valid_move = add_symbol(symbol, pos)
        if not valid_move:
            print("Position is invalid!")
    
    draw_board()
    return check_game_over(board)

def reset_game():
    # Reset winner status
    global hasWinner
    hasWinner = False

    # Initialize board and reset, respectively
    global board
    board = np.zeros((3, 3))

def draw_board():
    size = board.shape[0]
    print()
    for i in range(size):
        for j in range(size):
            
            #  X | O | X
            # ---|---|---
            #  O | X | X
            # ---|---|---
            #  X | O | O
            
            if j != size - 1:
                print(f" {x_o(i,j)} |", end ="")
            else:
                print(f" {x_o(i,j)} ", end ="")
        print()
        if i != size - 1:
            print("---|---|---")
                
def x_o(i, j):
    """ Decodes a number into a "X" or "O" """
    if board[i][j] == 1:
        return "X"
    elif board[i][j] == 2:
        return "O"
    else:
        return " "

def add_symbol(symbol, pos):
    """ Adds a 1 to the board at position pos if symbol == "X"
        Adds a 2 to the board at position pos if symbol == "O"
        Returns true if the board has been updated successfully"""
    if symbol == "X":
        entry = 1
    elif symbol == "O":
        entry = 2
    
    # Board indices from 0 to 8 (left to right and top to bottom)
    board_pos = pos - 1

    # Intern representation                 Players/Users repr.
    # 0 1 2                                 1 2 3
    # 3 4 5                                 4 5 6
    # 6 7 8                                 7 8 9
       
    if board[board_pos // 3][board_pos % 3] != 0:
        return False
    
    board[board_pos // 3][board_pos % 3] = entry
    
    return True

def check_game_over(board, set_winner=True):
    """ Checks anyone has won the game or if it is a tie in which case True is returned
        set_winner allows to directly define the winner / a tie and end the game """
    size = board.shape[0]
    # Check all rows
    for i in range(size):
        if is_complete(board[i], set_winner):
            return True
    
    # Check all columns
    for i in range(size):
        if is_complete(np.transpose(board)[i], set_winner):
            return True

    # Check diagonals
    if (is_complete(np.array([board[0][0], board[1][1], board[2][2]]), set_winner) 
     or is_complete(np.array([board[2][0], board[1][1], board[0][2]]), set_winner)):
        return True

    # Check if all fields are filled (no free moves left) -> Tie
    if not get_free_moves():
        return True

    return False

def is_complete(line, set_winner):
    """ Returns true if the given array is full of one symbol type
        If set_winner is True, the winner data is set acordingly"""
    global hasWinner
    global winner_name
    global player_score_1
    global player_score_2

    if np.all(line == 1):
        if not set_winner:
            return True
        hasWinner = True
        winner_name = player_name_1
        player_score_1 += 1
    elif np.all(line == 2):
        if not set_winner:
            return True
        hasWinner = True
        winner_name = player_name_2
        player_score_2 += 1

    return hasWinner

# ======= Start of the game ========

print_welcome()
print_rules()

gmode = range_question("Choose '1' to play against the computer or '2' to play against another player: ", 2)

with_turns = yes_no_question("Take turns at every new game? (y/n): ")

# Player can choose a difficulty in single player mode
if gmode == 1:
    level = range_question("Select a level number (1 = 'easy', 2 = 'medium' or 3 = 'hard'): ", 3)

# Choose Player Names at the beginning
player_name_1 = name_question("Name of player 1 (X): ")
player_name_2 = name_question("Name of player 2 (O): ")

# Replay until chosen to stop 
while True:
    if gmode == 1:
        start_singleplayer_game()
    elif gmode == 2:
        start_multiplayer_game()

    print_ending()

    replay = yes_no_question("Play again (y/n)?: ")

    if replay == "n":
        break

    if with_turns == "y":
        second_starts = not second_starts

# ======= End of the Game ==========