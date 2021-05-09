from graphic_ui.menus.singleplayer_menu import singleplayer_menu
from graphic_ui.menus.multiplayer_menu import multiplayer_menu
from graphic_ui.menus.options_menu import options_menu
from graphic_ui.menus.credits_menu import credits_menu
import pygame
import pygame_menu
from graphic_ui.gui_consts import WIDTH, HEIGHT, THEME, ENGINE

screen = pygame.display.set_mode((WIDTH, HEIGHT))

menu = pygame_menu.Menu("Tic Tac Toe", WIDTH, HEIGHT, theme=THEME)

# Setup background music
pygame.mixer.music.load("sounds/almost_bliss.mp3")
# Play from beginning and repeat
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.pause()

bg_image = pygame_menu.BaseImage(image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_METAL)

def main_background():
    bg_image.draw(screen)

def menu_fun():
    menu.enable()
    menu.add.button("One Player", singleplayer_menu)
    menu.add.button("Two Players", multiplayer_menu)
    menu.add.button("Options", options_menu)
    menu.add.button("Credits", credits_menu)
    menu.add.label("")
    menu.add.button("Quit", pygame_menu.events.EXIT)

    if menu.is_enabled():
        menu.mainloop(screen, main_background)