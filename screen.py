import pygame
import colors
import sys

pygame.init()
clock = pygame.time.Clock()
size = (1366, 768)

screen = pygame.display.set_mode(size)
screen.fill(colors.WHITE)


def draw_circle(circle, color):
    return pygame.draw.circle(screen, color, circle.rect.center, 10)


def update(player, out):
    player.rect[1] -= player.movement[0]
    player.rect[1] += player.movement[1]
    player.rect[0] -= player.movement[2]
    player.rect[0] += player.movement[3]
    if player.rect[0] < 0:
        player.rect[0] = 0
    if player.rect[0] > 1346:
        player.rect[0] = 1346
    if player.rect[1] < 0:
        player.rect[1] = 0
    if player.rect[1] > 748:
        player.rect[1] = 748
    screen.fill(colors.WHITE)
    draw_circle(player, colors.PLAYER)
    draw_circle(out, colors.EXIT)


class Player(object):
    def __init__(self):
        self.color = colors.PLAYER
        self.rect = pygame.Rect(10, 10, 20, 20)
        self.movement = [0, 0, 0, 0]


class Exit(object):
    def __init__(self):
        self.color = colors.EXIT
        self.rect = pygame.Rect(1336, 738, 20, 20)


def quit_game():
    pygame.quit()
    sys.exit()


def game_loop():
    player = Player()
    out = Exit()
    screen.fill(colors.WHITE)
    while True:
        update(player, out)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.movement[0] = 1
                if event.key == pygame.K_DOWN:
                    player.movement[1] = 1
                if event.key == pygame.K_LEFT:
                    player.movement[2] = 1
                if event.key == pygame.K_RIGHT:
                    player.movement[3] = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.movement[0] = 0
                if event.key == pygame.K_DOWN:
                    player.movement[1] = 0
                if event.key == pygame.K_LEFT:
                    player.movement[2] = 0
                if event.key == pygame.K_RIGHT:
                    player.movement[3] = 0

        pygame.display.update()
        clock.tick(240)


def main():
    game_loop()


if __name__ == "__main__":
    main()
