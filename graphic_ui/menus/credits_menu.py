from graphic_ui.gui_consts import WIDTH, HEIGHT, THEME, ENGINE
import pygame
import pygame_menu

credits_menu = pygame_menu.Menu("Credits", WIDTH, HEIGHT, theme=THEME)   

credits_menu.add.label("Developer:\nJens Lemke\n \nSpecial Thanks:\nLilly Warzecha\n \n\
    Music:\n'Almost Bliss'\nKevin MacLeod (incompetech.com)\nLicensed under Creative Commons:\nBy Attribution 3.0\n \
    http://creativecommons.org/licenses/by/3.0/\n ")
credits_menu.add.button('Back', pygame_menu.events.BACK)
credits_menu.add.label("")