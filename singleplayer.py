# ----------- Single Player Game ----------------
import global_vars as gv
import game_logic as gl
import numpy as np
import random

def start_singleplayer_game(gmode, second_starts, level, level_p2=0, pc_vs_pc=False):
    """Core funcion of game implements the tic tac toe strategy (minmax algorithm)"""
    gm_over = False
    # Human player starts
    first_player = not second_starts
    gl.reset_game()
    gl.draw_board()

    while not gm_over:
        # Human's turn
        if first_player:
            gm_over = make_comp_move(first_player, level) if pc_vs_pc else gl.make_human_move(first_player)
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
       pos = random.choice(gl.get_free_moves(gv.board))
    # Medium
    elif level == 2:
        # Computer blocks and choses corners > middle > edge
        pos = medium_move()
    # Hard (Undefeatable)
    elif level == 3:
        # First two moves are chosen randomly so the human has a chance to win
        if len(gl.get_free_moves(gv.board)) in [8, 9]:
            pos = random.choice(gl.get_free_moves(gv.board))
        else:
            board_copy = np.copy(gv.board)
            pos = minimax(board_copy, symbol, symbol)['pos']

    gl.add_symbol(symbol, pos)
    print()
    print(f"{gv.player_name_1 if first_player else gv.player_name_2} has moved an '{symbol}' to position {pos}")
    gl.draw_board()
    return gl.check_game_over(gv.board)

def medium_move():
    free_moves = gl.get_free_moves(gv.board)

    # Check if any player is about to win with the next move: block it and take the win, respectively
    # 2 = "O" first: Winning has higher priority than blocking
    for sym in [2, 1]:
        for pos in free_moves:
            board_copy = np.copy(gv.board)
            board_pos = pos - 1
            board_copy[board_pos // 3][board_pos % 3] = sym
            if gl.check_game_over(board_copy, False, False):
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
    """ Implements the minimax algorithm to maximize the computers chance of winning """
    max_sym = own_symbol 
    other_sym = "X" if symbol == "O" else "O"
    free_moves = gl.get_free_moves(board_copy)

    # Check if game is over, set a winner but do not increase player score
    gl.check_game_over(board_copy, True, False)
    if gv.winner_name == (gv.player_name_1 if other_sym == "X" else gv.player_name_2):
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
        gl.reset_game(False)
        sim_score['pos'] = free_move

        if symbol == max_sym:
            if sim_score['score'] > best['score']:
                best = sim_score
        else:
            if sim_score['score'] < best['score']:
                best = sim_score
    return best
