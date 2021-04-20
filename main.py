import global_vars as gv
import print_messages as pm
import user_input as ui
import singleplayer as sp
import multiplayer as mp

# ======= Start of the game ========
if __name__ == '__main__':
    gv.init()
    pm.print_welcome()
    pm.print_rules()

    gmode = ui.range_question("Choose '1' to play against the computer, '2' to play against another player or '3' if 2 PCs shall play against each other: ", 3)

    # True if in this round the second player starts the game
    second_starts = False
    with_turns = ui.yes_no_question("Take turns at every new game? (y/n): ")

    # Player can choose a difficulty in single player mode
    if gmode == 1:
        # easy = 1 
        # medium = 2
        # hard = 3 
        level = ui.range_question("Select a level number (1 = 'easy', 2 = 'medium' or 3 = 'hard'): ", 3)

    # Two Computers play against each other
    if gmode == 3:
        level_p1 = ui.range_question("Select a level number for player 1 (1 = 'easy', 2 = 'medium' or 3 = 'hard'): ", 3)
        level_p2 = ui.range_question("Select a level number for player 2 (1 = 'easy', 2 = 'medium' or 3 = 'hard'): ", 3)

    # Choose Player Names at the beginning
    gv.player_name_1 = ui.name_question("Name of player 1 (X): ")
    gv.player_name_2 = ui.name_question("Name of player 2 (O): ")

    # Replay until chosen to stop 
    while True:
        if gmode == 1:
            sp.start_singleplayer_game(gmode, second_starts, level)
        elif gmode == 2:
            mp.start_multiplayer_game(second_starts)
        elif gmode == 3:
            sp.start_singleplayer_game(gmode, second_starts, level_p1, level_p2, True)

        pm.print_ending()

        # comment out wheter to manualy choose to play again
        replay = ui.yes_no_question("Play again (y/n)?: ")
        # replay = "y"

        if replay == "n":
            break

        if with_turns == "y":
            second_starts = not second_starts

# ======= End of the Game ==========