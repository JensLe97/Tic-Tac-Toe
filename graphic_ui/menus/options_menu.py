from graphic_ui.gui_consts import WIDTH, HEIGHT, THEME, CLICK, ENGINE
import global_vars as gv

import pygame
import pygame_menu

music_on = False

def set_sound(with_sound):
    from graphic_ui.menus.main_menu import menu
    if gv.sound_on:
        menu.set_sound(None, recursive=True)
    else:
        menu.set_sound(ENGINE, recursive=True)
    gv.sound_on = not gv.sound_on

def set_music(with_music):
    global music_on
    if music_on:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    music_on = not music_on
    
options_menu = pygame_menu.Menu("Options", WIDTH, HEIGHT, theme=THEME)

options_menu.add.toggle_switch('Sound Effects  ', False, onchange=set_sound)
options_menu.add.toggle_switch('Music  ', False, onchange=set_music)
options_menu.add.label("")
options_menu.add.button('Back', pygame_menu.events.BACK)