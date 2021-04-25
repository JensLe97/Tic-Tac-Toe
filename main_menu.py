from singleplayer_menu import singleplayer_menu
from multiplayer_menu import multiplayer_menu
from options_menu import options_menu
from credits_menu import credits_menu
import pygame
import pygame_menu
from gui_consts import WIDTH, HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
menu = pygame_menu.Menu("Tic Tac Toe", WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_BLUE)

def menu_fun():
    global menu
    menu.enable()
    menu.add.button("One Player", singleplayer_menu)
    menu.add.button("Two Players", multiplayer_menu)
    menu.add.button("Options", options_menu)
    menu.add.button("Credits", credits_menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    if menu.is_enabled():
        menu.mainloop(screen)

