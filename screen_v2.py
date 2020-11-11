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

ships = []


def draw_circle(circle, color):
    return pygame.draw.circle(screen, color, circle.rect.center, 10)


def update(player, out, boats):
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
    for boat in boats:
        if boat.rect[0] < -30 or boat.rect[0] > 1400 or boat.rect[1] < -30 or boat.rect[1] > 800:
            ships.remove(boat)
            continue
        boat.positions[1] -= boat.movement[0]
        boat.positions[1] += boat.movement[1]
        boat.positions[0] -= boat.movement[2]
        boat.positions[0] += boat.movement[3]
        boat.rect[0] = boat.positions[0]
        boat.rect[1] = boat.positions[1]
        draw_circle(boat, colors.BLACK)


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


def negative_x(ship):
    ship.rect = pygame.Rect(-20, random.randint(0, 768), 20, 20)
    ship.positions[0] = ship.rect[0]
    ship.positions[1] = ship.rect[1]
    ship.movement[3] = 1
    ship.movement[1] = random.random()
    ship.movement[0] = random.random()


def positive_x(ship):
    ship.rect = pygame.Rect(1390, random.randint(0, 768), 20, 20)
    ship.positions[0] = ship.rect[0]
    ship.positions[1] = ship.rect[1]
    ship.movement[2] = 1
    ship.movement[1] = random.random()
    ship.movement[0] = random.random()


def negative_y(ship):
    ship.rect = pygame.Rect(random.randint(0, 1366), -20, 20, 20)
    ship.positions[0] = ship.rect[0]
    ship.positions[1] = ship.rect[1]
    ship.movement[1] = 1
    ship.movement[3] = random.random()
    ship.movement[2] = random.random()


def positive_y(ship):
    ship.rect = pygame.Rect(random.randint(0, 1366), 790, 20, 20)
    ship.positions[0] = ship.rect[0]
    ship.positions[1] = ship.rect[1]
    ship.movement[0] = 1
    ship.movement[3] = random.random()
    ship.movement[2] = random.random()


class Ship(object):
    def __init__(self):
        spawn_points = {
            "negative_x": negative_x,
            "positive_x": positive_x,
            "negative_y": negative_y,
            "positive_y": positive_y
        }
        directions = ["negative_x", "negative_y", "positive_x", "positive_y"]
        chances = [0.25, 0.25, 0.25, 0.25]
        self.movement = [0, 0, 0, 0]
        self.positions = [0, 0]
        self.color = colors.BLACK
        self.rect = None
        spawn_points[random.choices(directions, chances)[0]](self)


def quit_game():
    global stop_thread
    stop_thread = True
    pygame.quit()
    sys.exit()


def ship_movement():
    global stop_thread
    global ships
    while True:
        if stop_thread:
            break
        ship = Ship()
        ships.append(ship)
        time.sleep(0.1)


def game_loop():
    player = Player()
    out = Exit()
    screen.fill(colors.WHITE)
    global ships

    global stop_thread
    stop_thread = False

    x = threading.Thread(target=ship_movement)
    x.start()

    while True:
        update(player, out, ships)
        print(len(ships))

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
