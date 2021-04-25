# ------------ Multiplayer Game --------------
import global_vars as gv
import game_logic as gl

def start_multiplayer_game(second_starts):
    """Core funcion of game for two players where each can decide where to place symbols"""
    # Reset Game logic
    gm_over = False
    # Wheter the first player ("X") starts the game or not
    first_player = not second_starts

    gl.reset_game()
    gl.draw_board()

    while not gm_over:
        gm_over = gl.make_human_move(first_player)
        
        first_player = not first_player
