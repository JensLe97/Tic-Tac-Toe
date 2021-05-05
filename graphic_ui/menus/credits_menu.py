from graphic_ui.gui_consts import WIDTH, HEIGHT, THEME, ENGINE
import pygame
import pygame_menu

credits_menu = pygame_menu.Menu("Credits", WIDTH, HEIGHT, theme=THEME)   

credits_menu.add.button('Back', pygame_menu.events.BACK)