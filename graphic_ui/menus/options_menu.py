from graphic_ui.gui_consts import WIDTH, HEIGHT
import pygame
import pygame_menu

def set_sound(with_sound):
    pass

options_menu = pygame_menu.Menu("Options", WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_BLUE)
options_menu.add.toggle_switch('Sound  ', False, onchange=set_sound)   
options_menu.add.button('Back', pygame_menu.events.BACK)