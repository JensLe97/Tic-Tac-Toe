# --------- Both Single and Multiplayer -------------
import global_vars as gv
import console.user_input as ui
import numpy as np

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
        pos = ui.range_question(f"{gv.player_name_1 if first_player else gv.player_name_2}, choose a position for '{symbol}': ", 9)
        valid_move = add_symbol(symbol, pos)
        if not valid_move:
            print("Position is invalid!")
    
    draw_board()
    return check_game_over(gv.board)

def reset_game(reset_board=True):
    # Reset winner status
    gv.hasWinner = False
    gv.winner_name = None

    # Initialize board and reset, respectively
    if reset_board:
        gv.board = np.zeros((3, 3))

def draw_board():
    size = gv.board.shape[0]
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
    if gv.board[i][j] == 1:
        return "X"
    elif gv.board[i][j] == 2:
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
       
    if gv.board[board_pos // 3][board_pos % 3] != 0:
        return False
    
    gv.board[board_pos // 3][board_pos % 3] = entry
    
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

    if np.all(line == 1):
        if not set_winner:
            return True
        gv.hasWinner = True
        gv.winner_name = gv.player_name_1
        if change_score:
            gv.player_score_1 += 1
    elif np.all(line == 2):
        if not set_winner:
            return True
        gv.hasWinner = True
        gv.winner_name = gv.player_name_2
        if change_score:
            gv.player_score_2 += 1

    return gv.hasWinner
