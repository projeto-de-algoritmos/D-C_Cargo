import time
import pygame
import colors
import sys
import random
import threading

pygame.init()
clock = pygame.time.Clock()
size = (1366, 768)
stop_thread = False

screen = pygame.display.set_mode(size)
screen.fill(colors.WHITE)


def draw_circle(circle, color):
    return pygame.draw.circle(screen, color, circle.rect.center, 10)


def update(player, out, ships):
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
    for ship in ships:
        ship.rect[1] -= ship.movement[0]
        ship.rect[1] += ship.movement[1]
        ship.rect[0] -= ship.movement[2]
        ship.rect[0] += ship.movement[3]
        draw_circle(ship, colors.BLACK)


class Player(object):
    def __init__(self):
        self.color = colors.PLAYER
        self.rect = pygame.Rect(10, 10, 20, 20)
        self.movement = [0, 0, 0, 0]
        self.points = 100


class Exit(object):
    def __init__(self):
        self.color = colors.EXIT
        self.rect = pygame.Rect(1336, 738, 20, 20)


def move_up(ship):
    ship.movement[0] = 1


def move_down(ship):
    ship.movement[1] = 1


def move_left(ship):
    ship.movement[2] = 1


def move_right(ship):
    ship.movement[3] = 1


def move_up_left(ship):
    ship.movement[0] = 1
    ship.movement[2] = 1


def move_up_right(ship):
    ship.movement[0] = 1
    ship.movement[3] = 1


def move_down_left(ship):
    ship.movement[1] = 1
    ship.movement[2] = 1


def move_down_right(ship):
    ship.movement[1] = 1
    ship.movement[3] = 1


class Ship(object):
    def __init__(self):
        self.color = colors.BLACK
        self.rect = pygame.Rect(670, 350, 20, 20)
        self.movement = [0, 0, 0, 0]
        self.moving = {
            "up": move_up,
            "down": move_down,
            "left": move_left,
            "right": move_right,
            "up-left": move_up_left,
            "up-right": move_up_right,
            "down-left": move_down_left,
            "down-right": move_down_right
        }


def quit_game():
    global stop_thread
    stop_thread = True
    pygame.quit()
    sys.exit()


def ship_movement(*ships):
    global stop_thread
    directions = ["up", "down", "left", "right", "up-left", "up-right", "down-left", "down-right"]
    chances = [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]
    while True:
        if stop_thread:
            break
        for ship in ships:
            ship.movement = [0, 0, 0, 0]
            mov = random.choices(directions, chances)
            ship.moving[mov[0]](ship)
            time.sleep(0.001)


def game_loop():
    ship_number = 100
    ships = []
    for i in range(ship_number):
        ships.append(Ship())
    player = Player()
    out = Exit()
    screen.fill(colors.WHITE)

    global stop_thread
    stop_thread = False

    x = threading.Thread(target=ship_movement, args=ships)
    x.start()

    while True:
        update(player, out, ships)

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
