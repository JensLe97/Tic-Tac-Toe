from gui_mode import play_gui
import pygame
import pygame_menu
from gui_consts import WIDTH, HEIGHT

singleplayer_menu = pygame_menu.Menu("One Player", WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_BLUE)   
singleplayer_menu.add.button("Play", play_gui, False)
singleplayer_menu.add.button('Back', pygame_menu.events.BACK)