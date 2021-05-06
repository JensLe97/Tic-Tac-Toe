from graphic_ui.gui_mode import play_gui
from graphic_ui.gui_consts import WIDTH, HEIGHT, COLORS, THEME, ENGINE
import global_vars as gv
import pygame
import pygame_menu

def set_player_1_name(name):
    gv.player_name_1 = name

def set_player_2_name(name):
    gv.player_name_2 = name
    
def set_first(selected_first, first_num):
    gv.first_value = first_num

def set_colors(selected_first, color_num):
    if color_num == 0:
        gv.colors = COLORS[:2]
    elif color_num == 1:
        gv.colors = COLORS[2:4]
    elif color_num == 2:
        gv.colors = COLORS[4:]

multiplayer_menu = pygame_menu.Menu("Two Players", WIDTH, HEIGHT, theme=THEME)


multiplayer_menu.add.text_input("First Player:  ", default="Player 1", maxchar=8, input_type=pygame_menu.locals.INPUT_TEXT, onchange=set_player_1_name)
multiplayer_menu.add.text_input("Opponent:  "    , default="Player 2", maxchar=8, input_type=pygame_menu.locals.INPUT_TEXT, onchange=set_player_2_name)

first = [("X", 3),
         ("O", 2),
         ("XO", 0)]
multiplayer_menu.add.selector(title="First Move:  ", items=first, onchange=set_first)

colors = [("Red/Green", 0),
         ("Blue/Yellow", 1),
         ("Black/White", 2)]
multiplayer_menu.add.selector(title="Colors:  ", items=colors, onchange=set_colors)

# Start Game with singleplayer = False
multiplayer_menu.add.button("Play", play_gui, False)
multiplayer_menu.add.label("")
multiplayer_menu.add.button('Back', pygame_menu.events.BACK)