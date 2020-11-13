import pygame
import random
import math
import time

import merge_sort as mg, closest_pair_of_points as closest, auxiliary as aux, colors

pygame.init()
clock = pygame.time.Clock()
size = (1366, 768)
level = 1

menu = pygame.image.load('../src/images/menu.png')
players_img = pygame.image.load('../src/images/ship-player.png')
ships_img = pygame.image.load('../src/images/ships.png')
port_img = pygame.image.load('../src/images/port.png')
pygame.display.set_caption("Cargo")
icon = pygame.image.load('../src/images/icon.png')
pygame.display.set_icon(icon)

screen = pygame.display.set_mode(size)
screen.fill(colors.WHITE)


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
            "negative_x": aux.negative_x,
            "positive_x": aux.positive_x,
            "negative_y": aux.negative_y,
            "positive_y": aux.positive_y
        }
        directions = ["negative_x", "negative_y", "positive_x", "positive_y"]
        chances = [0.25, 0.25, 0.25, 0.25]
        self.velocity = [0, 0, 0, 0]
        self.positions = [0, 0]
        self.color = colors.BLACK
        self.rect = pygame.Rect(0, 0, 20, 20)
        spawn_points[random.choices(directions, chances)[0]](self)


def get_x_coordinates(ships, player):
    temp = []
    for ship in ships:
        temp.append((ship.rect[0], ship.rect[1]))
    temp.append((player.rect[0], player.rect[1]))
    return temp


def collision(ships, ordered_array, player, time_elapsed):
    if ships:
        pair = closest.closest_pair(ordered_array)
        p1 = pair[0]
        p2 = pair[1]
        if p1 and math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) < 30:
            if time.perf_counter() - time_elapsed < 1.5:
                return
            elif p1 == (player.rect[0], player.rect[1]) or p2 == (player.rect[0], player.rect[1]):
                restart_game_window(False)
            for x in ships:
                if (x.rect[0], x.rect[1]) == p1:
                    ships.remove(x)
                    break
            for x in ships:
                if (x.rect[0], x.rect[1]) == p2:
                    ships.remove(x)
                    break


def menu_window():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                aux.quit_game()

        screen.fill(colors.WHITE)
        screen.blit(menu, (0, 0))


        aux.button(screen, 'START', 590, 450, 200, 100, colors.BRIGHT_GREEN, game_loop)
        pygame.display.update()
        clock.tick(15)


def restart_game_window(win):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                aux.quit_game()

        if win and level == 5:
            finish_game_window()

        aux.button(screen, 'RESTART', 510, 450, 100, 50, colors.GREEN, game_loop)
        if win:
            aux.game_win_text(screen)
            aux.button(screen, 'NEXT', 630, 450, 100, 50, colors.BLUE, next_level)
        else:
            aux.game_lose_text(screen)
        aux.button(screen, 'QUIT', 750, 450, 100, 50, colors.RED, aux.quit_game)

        pygame.display.update()
        clock.tick(15)


def finish_game_window():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                aux.quit_game()

        aux.game_finish_text(screen)
        aux.button(screen, 'QUIT', 630, 450, 100, 50, colors.RED, aux.quit_game)

        pygame.display.update()
        clock.tick(15)


# increase difficulty
def next_level():
    global level
    level += 1
    game_loop()


def game_loop():
    elapsed = time.perf_counter()
    player = Player()
    out = Exit()
    screen.fill(colors.WHITE)
    loop_counter = 0
    ships = []
    levels = {
        1: 100,
        2: 50,
        3: 25,
        4: 13,
        5: 7,
        6: finish_game_window
    }

    while True:
        update(player, out, ships)
        if loop_counter == levels[level]:
            ships.append(Ship())
            loop_counter = 0
        else:
            ordered_array = mg.merge_sort(get_x_coordinates(ships, player))
            collision(ships, ordered_array, player, elapsed)

        if math.sqrt((player.rect[0] - out.rect[0]) ** 2 + (player.rect[1] - out.rect[1]) ** 2) < 30:
            restart_game_window(True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                aux.quit_game()
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
    menu_window()
    game_loop()


if __name__ == "__main__":
    main()
