from graphic_ui.gui_mode import play_gui
from graphic_ui.gui_consts import WIDTH, HEIGHT, COLORS, THEME, ENGINE
import global_vars as gv
import pygame
import pygame_menu

def set_player_1_name(name):
    gv.player_name_1 = name

def set_player_2_name(name):
    gv.player_name_2 = name

def set_level(selected_level, lvl_num):
    gv.level = lvl_num
    if lvl_num == 4:
        # Insert selectors for the PCs difficulties
        s1 = singleplayer_menu.add.selector(title="Level PC 1:  ", items=levels[:-1], onchange=set_level_p1, selector_id="lvlp1")
        singleplayer_menu.move_widget_index(s1, 3)
        s2 = singleplayer_menu.add.selector(title="Level PC 2:  ", items=levels[:-1], onchange=set_level_p2, selector_id="lvlp2")
        singleplayer_menu.move_widget_index(s2, 4)
    else:
        if isinstance(singleplayer_menu.get_widget("lvlp1"), pygame_menu.widgets.widget.selector.Selector):
            singleplayer_menu.remove_widget(singleplayer_menu.get_widget("lvlp1"))
            singleplayer_menu.remove_widget(singleplayer_menu.get_widget("lvlp2"))

def set_level_p1(selected_level, lvl_num):
    gv.level_p1 = lvl_num

def set_level_p2(selected_level, lvl_num):
    gv.level_p2 = lvl_num

def set_first(selected_first, first_num):
    gv.first_value = first_num

def set_colors(selected_first, color_num):
    if color_num == 0:
        gv.colors = COLORS[:2]
    elif color_num == 1:
        gv.colors = COLORS[2:4]
    elif color_num == 2:
        gv.colors = COLORS[4:]

singleplayer_menu = pygame_menu.Menu("One Player", WIDTH, HEIGHT, theme=THEME)

singleplayer_menu.add.text_input("First Player (Me):  ", default="Player 1", maxchar=8, input_type=pygame_menu.locals.INPUT_TEXT, onchange=set_player_1_name)
singleplayer_menu.add.text_input("Opponent:  "         , default="Player 2", maxchar=8, input_type=pygame_menu.locals.INPUT_TEXT, onchange=set_player_2_name)

levels = [("Easy", 1),
         ("Medium", 2),
         ("Hard", 3),
         ("PC vs PC", 4)]
singleplayer_menu.add.selector(title="Level:  ", items=levels, onchange=set_level)

first = [("X", 3),
         ("O", 2),
         ("XO", 0)]
singleplayer_menu.add.selector(title="First Move:  ", items=first, onchange=set_first)

colors = [("Red/Green", 0),
         ("Blue/Yellow", 1),
         ("Black/White", 2)]
singleplayer_menu.add.selector(title="Colors:  ", items=colors, onchange=set_colors)

# Start Game with singleplayer = True
singleplayer_menu.add.button("Play", play_gui, True)
singleplayer_menu.add.label("")
singleplayer_menu.add.button('Back', pygame_menu.events.BACK)