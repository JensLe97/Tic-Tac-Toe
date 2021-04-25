import pygame
import global_vars as gv
from gui_consts import CIRCLE_COLOR, CROSS_COLOR
pygame.font.init()

COLOR_LIGHT = (102, 204, 255)
COLOR_DARK = (51, 153, 255)
COLOR_CLICKED = (0, 0, 200)
TEXT_COLOR = (0, 0, 100)

font = pygame.font.SysFont('cambria', 35)

def draw_button(text, screen, rect):
    img = font.render(text, True, TEXT_COLOR)
    # Mouse has click the button
    if check_clicked(rect):
        pygame.draw.rect(screen, COLOR_CLICKED, rect)
        # Pause to show the clicked button
        pygame.display.update()
        pygame.time.delay(50)
    # Mouse hovers over button
    elif check_mouse_on_button(rect):
        pygame.draw.rect(screen, COLOR_DARK, rect)
    else:
        pygame.draw.rect(screen, COLOR_LIGHT, rect)

    screen.blit(img, (rect.x + (rect.width - img.get_width()) // 2, rect.y + (rect.height - img.get_height()) // 2))
    
def check_mouse_on_button(rect):
    pos = pygame.mouse.get_pos()
    return rect.collidepoint(pos)

def check_clicked(rect):
    click = pygame.mouse.get_pressed()
    return check_mouse_on_button(rect) and click[0]

def draw_winner_name(winner, screen, rect):
    img = font.render(winner, True, TEXT_COLOR)
    pygame.draw.rect(screen, COLOR_LIGHT, rect)

    screen.blit(img, (rect.x + (rect.width - img.get_width()) // 2, rect.y + (rect.height - img.get_height()) // 2))

def draw_scores(screen, rect, first_player):
    scores = font.render(f" {gv.player_name_1}: {gv.player_score_1}      {gv.player_name_2}: {gv.player_score_2}", True, TEXT_COLOR)
    if first_player:
        font.set_underline(True)
        x_sym = font.render("X", True, CROSS_COLOR)
        font.set_underline(False)
        o_sym = font.render("O", True, CIRCLE_COLOR)
    else:
        font.set_underline(True)
        o_sym = font.render("O", True, CIRCLE_COLOR)
        font.set_underline(False)
        x_sym = font.render("X", True, CROSS_COLOR)

    screen.blit(scores, (rect.x + (rect.width - scores.get_width()) // 2, rect.y + (rect.height - scores.get_height()) // 2))
    screen.blit(x_sym, (rect.x - x_sym.get_width() + (rect.width - scores.get_width()) // 2, rect.y + (rect.height - scores.get_height()) // 2))
    screen.blit(o_sym, (rect.x + rect.width // 2, rect.y + (rect.height - scores.get_height()) // 2))
