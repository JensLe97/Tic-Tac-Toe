from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'HIDE'
import pygame_menu
import pygame
pygame.init()

# Window
WIDTH = 700
HEIGHT = WIDTH
MARGIN = WIDTH // 10

FPS = 60

# Board
SQUARE_SIZE = (WIDTH - 2 * MARGIN) // 3
LINE_WIDTH = SQUARE_SIZE // 15

# Symbols
SQUARE_MARGIN = SQUARE_SIZE // 6
CROSS_WIDTH = int(LINE_WIDTH * 3)
CIRCLE_WIDTH = int(CROSS_WIDTH // 1.5)
CIRLE_RADIUS = SQUARE_SIZE // 2.8

# Colors
GREEN = (0, 150, 0)
RED = (255, 50, 0) 
YELLOW = (235, 235, 0)
DARK_BLUE = (0, 0, 100)
LIGHT_BLUE = (204, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BG_COLOR = (140, 140, 140)
BOARD_COLOR = DARK_BLUE

COLORS = [GREEN, RED, DARK_BLUE, YELLOW, BLACK, WHITE]

# In-Game Font
font = pygame.font.SysFont('candara', 35, bold=True)

# Colors for buttons
COLOR_LIGHT = (128, 128, 128)
COLOR_DARK = (89, 89, 89)
COLOR_CLICKED = (64, 64, 64)
TEXT_COLOR = (255, 255, 255)

# Button dimensions
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 50

BACK_BUTTON_WIDTH = 100
BACK_BUTTON_HEIGHT = 50

# Scores
SCORE_MARGIN = MARGIN // 2
SCORE_WIDTH = 500
SCORE_HEIGHT = 50

# Menu Theme
MENU_FONT = pygame_menu.font.FONT_OPEN_SANS
THEME = pygame_menu.themes.THEME_DARK.copy()
THEME.set_background_color_opacity(0.5)
THEME.title_background_color=(0, 0, 0, 50)
THEME.widget_font=MENU_FONT
THEME.title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY_DIAGONAL
THEME.widget_font_color=(0,0,0)
THEME.selection_color=(255, 255, 255)

# Sounds
DRAW = pygame.mixer.Sound("sounds/draw.ogg")
CLICK = pygame.mixer.Sound("sounds/click.ogg")

ENGINE = pygame_menu.sound.Sound()
ENGINE.load_example_sounds()
ENGINE.set_sound(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, None)
ENGINE.set_sound(pygame_menu.sound.SOUND_TYPE_WIDGET_SELECTION, 'sounds/click.ogg', volume=1)
ENGINE.set_sound(pygame_menu.sound.SOUND_TYPE_KEY_ADDITION, 'sounds/draw.ogg', volume=1)