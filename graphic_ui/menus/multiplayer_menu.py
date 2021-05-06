from graphic_ui.gui_mode import play_gui
from graphic_ui.gui_consts import WIDTH, HEIGHT, COLORS, THEME, ENGINE
import global_vars as gv
import pygame
import pygame_menu

def set_player_1_name(selected_name, name="Player 1"):
    gv.player_name_1 = name if name in "Player 1" else selected_name

def set_player_2_name(selected_name, name="Player 2"):
    gv.player_name_2 = name if name in "Player 2" else selected_name
    
def set_first(selected_first, first_num):
    gv.first_value = first_num

def set_colors(selected_color, color_num):
    if color_num == 0:
        gv.colors = COLORS[:2]
    elif color_num == 1:
        gv.colors = COLORS[2:4]
    elif color_num == 2:
        gv.colors = COLORS[4:]

def update_widgets(w_1, w_2, w_3, w_4):
    """ Updates the states (global variables) of the text input fields and the selectors.
    When changing from single to multiplayer, widgets that are not changed again,
    are not updated automatically and the old value from the other menu is used. 
    Therefore, this method updates these states again.
    w_1/w_2: text_input player_name_1/2
    w_3:     selector for first player
    w_4:     selector for colors """
    w_1.change(w_1.get_value())
    w_2.change(w_2.get_value())
    w_3.change(w_3.get_value()[0][1])
    w_4.change(w_4.get_value()[0][1])

    # Start Game with singleplayer = False
    play_gui(False)

multiplayer_menu = pygame_menu.Menu("Two Players", WIDTH, HEIGHT, theme=THEME)

w_1 = multiplayer_menu.add.text_input("First Player:  ", default="Player 1", maxchar=8, input_type=pygame_menu.locals.INPUT_TEXT, onchange=set_player_1_name)
w_2 = multiplayer_menu.add.text_input("Opponent:  "    , default="Player 2", maxchar=8, input_type=pygame_menu.locals.INPUT_TEXT, onchange=set_player_2_name)

first = [("X", 3),
         ("O", 2),
         ("XO", 0)]
w_3 = multiplayer_menu.add.selector(title="First Move:  ", items=first, onchange=set_first)

colors = [("Red/Green", 0),
         ("Blue/Yellow", 1),
         ("Black/White", 2)]
w_4 = multiplayer_menu.add.selector(title="Colors:  ", items=colors, onchange=set_colors)

multiplayer_menu.add.button("Play", update_widgets, w_1, w_2, w_3, w_4)
multiplayer_menu.add.label("")
multiplayer_menu.add.button('Back', pygame_menu.events.BACK)