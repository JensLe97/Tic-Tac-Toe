import pygame
import pygame_menu
from gui_consts import WIDTH, HEIGHT

options_menu = pygame_menu.Menu("Options", WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_BLUE)   
options_menu.add.button('Back', pygame_menu.events.BACK)