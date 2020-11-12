import pygame
import colors
import sys
import random
import merge_sort as mg
import closest_pair_of_points as closest
import math
import time

pygame.init()
clock = pygame.time.Clock()
size = (1366, 768)

players_img = pygame.image.load('ship-player.png')
ships_img = pygame.image.load('ships.png')
port_img = pygame.image.load('port.png')

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
    elif player.rect[0] > 1346:
        player.rect[0] = 1346
    elif player.rect[1] < 0:
        player.rect[1] = 0
    elif player.rect[1] > 748:
        player.rect[1] = 748
    screen.fill(colors.BRIGHT_GREEN)
    screen.blit(players_img, player)
    screen.blit(port_img, out)
    for ship in ships:
        if ship.rect[0] < -30 or ship.rect[0] > 1400 or ship.rect[1] < -30 or ship.rect[1] > 800:
            ships.remove(ship)
            continue
        ship.positions[1] -= ship.velocity[0]
        ship.positions[1] += ship.velocity[1]
        ship.positions[0] -= ship.velocity[2]
        ship.positions[0] += ship.velocity[3]
        ship.rect[0] = ship.positions[0]
        ship.rect[1] = ship.positions[1]
        screen.blit(ships_img, ship)


class Player(object):
    def __init__(self):
        self.color = colors.PLAYER
        self.rect = pygame.Rect(10, 10, 20, 20)
        self.movement = [0, 0, 0, 0]


class Exit(object):
    def __init__(self):
        self.color = colors.EXIT
        self.rect = pygame.Rect(1298, 698, 20, 20)


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
        self.velocity = [0, 0, 0, 0]
        self.positions = [0, 0]
        self.color = colors.BLACK
        self.rect = pygame.Rect(0, 0, 20, 20)
        spawn_points[random.choices(directions, chances)[0]](self)


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


def get_x_coordinates(ships, player):
    temp = []
    for ship in ships:
        temp.append((ship.rect[0], ship.rect[1]))
    temp.append((player.rect[0], player.rect[1]))
    return temp


def collision(ships, ordered_array, player):
    if ships:
        pair = closest.closest_pair(ordered_array)
        p1 = pair[0]
        p2 = pair[1]
        if p1 and math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) < 30:
            if time.process_time() < 3:
                return
            elif p1 == (player.rect[0], player.rect[1]) or p2 == (player.rect[0], player.rect[1]):
                quit_game()
            for x in ships:
                if (x.rect[0], x.rect[1]) == p1:
                    ships.remove(x)
                    break
            for x in ships:
                if (x.rect[0], x.rect[1]) == p2:
                    ships.remove(x)
                    break


def game_loop():
    player = Player()
    out = Exit()
    screen.fill(colors.WHITE)
    loop_counter = 0
    ships = []

    while True:
        update(player, out, ships)
        if loop_counter == 100:
            ships.append(Ship())
            loop_counter = 0
        ordered_array = mg.merge_sort(get_x_coordinates(ships, player))
        collision(ships, ordered_array, player)

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
        loop_counter += 1


def main():
    game_loop()


if __name__ == "__main__":
    main()
