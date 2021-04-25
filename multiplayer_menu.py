from gui_mode import play_gui
import pygame
import pygame_menu
from gui_consts import WIDTH, HEIGHT

multiplayer_menu = pygame_menu.Menu("Two Players", WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_BLUE)   
multiplayer_menu.add.button("Play", play_gui, False)
multiplayer_menu.add.button('Back', pygame_menu.events.BACK)