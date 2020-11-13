import pygame
from src import colors
import random
import sys


# auxiliary function for customizing text
def text_hollow(font, message, font_color):
    not_color = [c ^ 0xFF for c in font_color]
    base = font.render(message, 0, font_color, not_color)
    size = base.get_width() + 2, base.get_height() + 2
    img = pygame.Surface(size, 16)
    img.fill(not_color)
    base.set_colorkey(0)
    img.blit(base, (0, 0))
    img.blit(base, (2, 0))
    img.blit(base, (0, 2))
    img.blit(base, (2, 2))
    base.set_colorkey(0)
    base.set_palette_at(1, not_color)
    img.blit(base, (1, 1))
    img.set_colorkey(not_color)
    return img


# auxiliary function for customizing text
def text_outline(font, message, font_color, outline_color):
    base = font.render(message, 0, font_color)
    outline = text_hollow(font, message, outline_color)
    img = pygame.Surface(outline.get_size(), 16)
    img.blit(base, (1, 1))
    img.blit(outline, (0, 0))
    img.set_colorkey(0)
    return img


def game_win_text(screen):
    win_text = text_outline(pygame.font.SysFont('default', 150), 'YOU WIN!', colors.WHITE, colors.BLACK)
    screen.blit(win_text, (430, 300))


def game_lose_text(screen):
    win_text = text_outline(pygame.font.SysFont('default', 150), 'YOU LOSE!', colors.WHITE, colors.BLACK)
    screen.blit(win_text, (410, 300))


def game_finish_text(screen):
    win_text = text_outline(pygame.font.SysFont('default', 150), 'CONGRATULATIONS!', colors.WHITE, colors.BLACK)
    screen.blit(win_text, (130, 300))


def negative_x(ship):
    ship.positions[0] = -20
    ship.positions[1] = random.randint(0, 768)
    ship.velocity[3] = 1
    ship.velocity[1] = random.random()
    ship.velocity[0] = random.random()


def positive_x(ship):
    ship.positions[0] = 1390
    ship.positions[1] = random.randint(0, 768)
    ship.velocity[2] = 1
    ship.velocity[1] = random.random()
    ship.velocity[0] = random.random()


def negative_y(ship):
    ship.positions[0] = random.randint(0, 1366)
    ship.positions[1] = -20
    ship.velocity[1] = 1
    ship.velocity[3] = random.random()
    ship.velocity[2] = random.random()


def positive_y(ship):
    ship.positions[0] = random.randint(0, 1366)
    ship.positions[1] = 790
    ship.velocity[0] = 1
    ship.velocity[3] = random.random()
    ship.velocity[2] = random.random()


def quit_game():
    pygame.quit()
    sys.exit()


def text_objects(text, font):
    text_surface = font.render(text, True, colors.NODE)
    return text_surface, text_surface.get_rect()


def button(screen, msg, x, y, w, h, ic, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, (ic[0], ic[1] - 20, ic[2] - 20), (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    small_text = pygame.font.SysFont("default", 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)