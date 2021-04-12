import numpy as np

# ========== Global variables for Game Logic =============
# True if there is a winner, False if it is a tie
hasWinner = False
winner_name = None

# Wheter or not players take turns at the beginning of each game
with_turns = False
# True if in this round the second player starts the game
second_starts = False

player_name_1 = None
player_name_2 = None

board = np.zeros((3, 3))

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

# ====== User Input ========

def range_question(question, number):
    """Asks the user to select a number beween 1 and number and returns it as int"""
    while True:
        print()
        n = int(input(question))

        if n in range(1, number + 1):
            return n
        else:
            print("Please choose a valid game mode!")

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

def start_singleplayer_game():
    """Core funcion of game implements the tic tac toe strategy (minmax algorithm)"""
    print("NOT IMPLEMENTED YET")

def start_multiplayer_game():
    """Core funcion of game for two players where each can decide where to place symbols"""
    gm_over = False
    first_player = not second_starts

    global hasWinner
    hasWinner = False

    # Initialize board and reset, respectively
    global board
    board = np.zeros((3, 3))
    draw_board()

    while not gm_over:
        symbol = "X" if first_player else "O"
        valid_move = False
        while not valid_move:
            pos = range_question(f"{player_name_1 if first_player else player_name_2}, choose a position for '{symbol}': ", 9)
            valid_move = add_symbol(symbol, pos)
            if not valid_move:
                print("Position is invalid!")

        draw_board()

        first_player = not first_player

        gm_over = check_game_over()

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

def check_game_over():
    """Checks anyone has won the game or if it is a tie in which case True is returned"""
    size = board.shape[0]
    # Check all rows
    for i in range(size):
        if is_complete(board[i]):
            return True
    
    # Check all columns
    for i in range(size):
        if is_complete(np.transpose(board)[i]):
            return True

    # Check diagonals
    if (is_complete(np.array([board[0][0], board[1][1], board[2][2]])) 
     or is_complete(np.array([board[2][0], board[1][1], board[0][2]]))):
        return True

    # Check if all fields are filled
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                return False

    return True

def is_complete(line):
    global hasWinner
    global winner_name

    if np.all(line == 1):
        hasWinner = True
        winner_name = player_name_1
    elif np.all(line == 2):
        hasWinner = True
        winner_name = player_name_2

    return hasWinner

# ======= Start of the game ========

print_welcome()
print_rules()

gmode = range_question("Choose '1' to play against the computer or '2' to play against another player: ", 2)

with_turns = yes_no_question("Take turns at every new game? (y/n): ")

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