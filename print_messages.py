# ======== Print Messages ===========
import global_vars as gv

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
    if gv.hasWinner:
        print(f"{gv.winner_name} wins!")
    else:
        print("Tie!")
    print()
    print(f"Scores -- {gv.player_name_1}: {gv.player_score_1}, {gv.player_name_2}: {gv.player_score_2}")