import pygame
import pygame_menu
from gui_consts import WIDTH, HEIGHT

credits_menu = pygame_menu.Menu("Credits", WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_BLUE)   
credits_menu.add.button('Back', pygame_menu.events.BACK)