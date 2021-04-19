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

# PC vs PC?
pc_vs_pc = False

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
level_p1 = 0
level_p2 = 0

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

def start_singleplayer_game(gmode):
    """Core funcion of game implements the tic tac toe strategy (minmax algorithm)"""
    gm_over = False
    # Human player starts
    first_player = not second_starts
    reset_game()
    draw_board()

    while not gm_over:
        # Human's turn
        if first_player:
            gm_over = make_comp_move(first_player, level_p1) if pc_vs_pc else make_human_move(first_player)
        # Computer's turn
        else:
            if gmode == 1:
                gm_over = make_comp_move(first_player, level)
            else:
                gm_over = make_comp_move(first_player, level_p2)

        first_player = not first_player

def make_comp_move(first_player, level):
    # own symbol
    symbol = "O" if not first_player else "X"
    # Easy
    if level == 1:
       pos = random.choice(get_free_moves(board))
    # Medium
    elif level == 2:
        # Computer blocks and choses corners > middle > edge
        pos = medium_move()
    # Hard (Undefeatable)
    elif level == 3:
        if len(get_free_moves(board)) == 9:
            pos = random.choice(get_free_moves(board))
        else:
            board_copy = np.copy(board)
            pos = minimax(board_copy, symbol, symbol)['pos']

    add_symbol(symbol, pos)
    print()
    print(f"{player_name_1 if first_player else player_name_2} has moved an '{symbol}' to position {pos}")
    draw_board()
    return check_game_over(board)

def medium_move():
    free_moves = get_free_moves(board)

    # Check if any player is about to win with the next move: block it and take the win, respectively
    # 2 = "O" first: Winning has higher priority than blocking
    for sym in [2, 1]:
        for pos in free_moves:
            board_copy = np.copy(board)
            board_pos = pos - 1
            board_copy[board_pos // 3][board_pos % 3] = sym
            if check_game_over(board_copy, False, False):
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

def minimax(board_copy, symbol, own_symbol):
    # Implements the minimax algorithm to maximize the computers chance of winning
    # Computer is player 2 = "O"
    # symbol always equals "O"
    max_sym = own_symbol 
    other_sym = "X" if symbol == "O" else "O"
    free_moves = get_free_moves(board_copy)

    global hasWinner
    global winner_name

    # Check if game is over, set a winner but do not increase player score
    check_game_over(board_copy, True, False)
    if winner_name == (player_name_1 if other_sym == "X" else player_name_2):
        return {'pos': None, 'score': 1 * (len(free_moves) + 1) if other_sym == max_sym else -1 * (len(free_moves) + 1)}
    elif not free_moves:
        return {'pos': None, 'score': 0}
    
    # Game is not over
    # Max max_sym starting from -infinity
    if symbol == max_sym:
        best = {'pos': None, 'score': np.NINF}
    # Min other player starting from infinity
    else:
        best = {'pos': None, 'score': np.Inf}
    
    # Try all possible moves and set best accordingly
    for free_move in free_moves:
        board_pos = free_move - 1
        board_copy[board_pos // 3][board_pos % 3] = 2 if symbol == "O" else 1
        sim_score = minimax(board_copy, other_sym, own_symbol)

        # Undo the move
        board_copy[board_pos // 3][board_pos % 3] = 0
        reset_game(False)
        sim_score['pos'] = free_move

        if symbol == max_sym:
            if sim_score['score'] > best['score']:
                best = sim_score
        else:
            if sim_score['score'] < best['score']:
                best = sim_score
    return best

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

def get_free_moves(board):
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

def reset_game(reset_board=True):
    # Reset winner status
    global hasWinner
    global winner_name
    hasWinner = False
    winner_name = None

    # Initialize board and reset, respectively
    if reset_board:
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

def check_game_over(board, set_winner=True, change_score=True):
    """ Checks anyone has won the game or if it is a tie in which case True is returned
        set_winner allows to directly define the winner / a tie and end the game """
    size = board.shape[0]
    # Check all rows
    for i in range(size):
        if is_complete(board[i], set_winner, change_score):
            return True
    
    # Check all columns
    for i in range(size):
        if is_complete(np.transpose(board)[i], set_winner, change_score):
            return True

    # Check diagonals
    if (is_complete(np.array([board[0][0], board[1][1], board[2][2]]), set_winner, change_score) 
     or is_complete(np.array([board[2][0], board[1][1], board[0][2]]), set_winner, change_score)):
        return True

    # Check if all fields are filled (no free moves left) -> Tie
    if not get_free_moves(board):
        return True

    return False

def is_complete(line, set_winner, change_score):
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
        if change_score:
            player_score_1 += 1
    elif np.all(line == 2):
        if not set_winner:
            return True
        hasWinner = True
        winner_name = player_name_2
        if change_score:
            player_score_2 += 1

    return hasWinner

# ======= Start of the game ========

print_welcome()
print_rules()

gmode = range_question("Choose '1' to play against the computer, '2' to play against another player or '3' if 2 PCs shall play against each other: ", 3)

with_turns = yes_no_question("Take turns at every new game? (y/n): ")

# Player can choose a difficulty in single player mode
if gmode == 1:
    level = range_question("Select a level number (1 = 'easy', 2 = 'medium' or 3 = 'hard'): ", 3)
if gmode == 3:
    level_p1 = range_question("Select a level number for player 1 (1 = 'easy', 2 = 'medium' or 3 = 'hard'): ", 3)
    level_p2 = range_question("Select a level number for player 2 (1 = 'easy', 2 = 'medium' or 3 = 'hard'): ", 3)

# Choose Player Names at the beginning
player_name_1 = name_question("Name of player 1 (X): ")
player_name_2 = name_question("Name of player 2 (O): ")

# Replay until chosen to stop 
while True:
    if gmode == 1:
        start_singleplayer_game(gmode)
    elif gmode == 2:
        start_multiplayer_game()
    elif gmode == 3:
        pc_vs_pc = True
        start_singleplayer_game(gmode)

    print_ending()

    # comment out wheter to manualy choose to play again
    replay = yes_no_question("Play again (y/n)?: ")
    # replay = "y"

    if replay == "n":
        break

    if with_turns == "y":
        second_starts = not second_starts

# ======= End of the Game ==========