import pygame
from enemies import Zombie, Wizard, Warrior
from tower import Tower, IceTower, FireTower, PlantTower
from board import Board
import random

pygame.init()


def scan_level(level_file_name):
    file = open(level_file_name + ".txt", encoding="utf-8").read().split("\n")
    file = list(map(list, file[:-1]))
    return len(file[0]), len(file), file


screen = pygame.display.set_mode((600, 600))
board = Board(*scan_level("new_level"), screen)
pygame.mixer.music.load('sounds\soundtrack.mp3')
pygame.mixer.music.play(-1)
running = True
screen.fill((71, 45, 23))
board.render()
all_enemies = pygame.sprite.Group()
all_towers = pygame.sprite.Group()
clock = pygame.time.Clock()
pygame.display.flip()
current_time = 0
enemies_left = board.current_wave * 5
hand = False
play = True
while running:
    current_time += 1
    if enemies_left != 0 and current_time % board.fps == 0:
        enemies_left -= 1
        if board.current_wave <= 5:
            enemy = Zombie(all_enemies, board)
        elif 3 < board.current_wave <= 10:
            enemy = random.choice([1, 2])
            if enemy == 1:
                enemy = Zombie(all_enemies, board)
            else:
                enemy = Wizard(all_enemies, board)
        else:
            enemy = random.choice([1, 2, 3])
            if enemy == 1:
                enemy = Zombie(all_enemies, board)
            elif enemy == 2:
                enemy = Wizard(all_enemies, board)
            else:
                enemy = Warrior(all_enemies, board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if event.button == 1:
                if 0 <= pos[0] <= 40 and 0 <= pos[1] <= 40:
                    if not hand and board.current_money >= 5:
                        board.current_money -= 5
                        hand = "fire"
                    elif hand:
                        board.current_money += 5
                        hand = False
                elif 60 <= pos[0] <= 100 and 0 <= pos[1] <= 40:
                    if not hand and board.current_money >= 10:
                        board.current_money -= 10
                        hand = "ice"
                    elif hand:
                        board.current_money += 10
                        hand = False
                elif 120 <= pos[0] <= 160 and 0 <= pos[1] <= 40:
                    if not hand and board.current_money >= 10:
                        board.current_money -= 20
                        hand = "plant"
                    elif hand:
                        board.current_money += 20
                        hand = False
                elif 480 <= pos[0] <= 538 and 0 <= pos[1] <= 60:
                    if play:
                        pygame.mixer.music.pause()
                        play = False
                    else:
                        play = True
                        pygame.mixer.music.unpause()

                if board.clicked(pos[0], pos[1]) and \
                        board.board[(pos[1] - board.offset[1]) // 30][(pos[0] - board.offset[0]) // 30] == '#':
                    if hand:
                        if hand == "fire":
                            tower = FireTower(all_towers, board, (pos[0] // 30 * 30, pos[1] // 30 * 30))
                            board.board[(pos[1] - board.offset[1]) // 30][(pos[0] - board.offset[0]) // 30] = 'F'
                        elif hand == "ice":
                            tower = IceTower(all_towers, board, (pos[0] // 30 * 30, pos[1] // 30 * 30))
                            board.board[(pos[1] - board.offset[1]) // 30][(pos[0] - board.offset[0]) // 30] = 'I'
                        elif hand == "plant":
                            tower = PlantTower(all_towers, board, (pos[0] // 30 * 30, pos[1] // 30 * 30))
                            board.board[(pos[1] - board.offset[1]) // 30][(pos[0] - board.offset[0]) // 30] = 'P'
                        hand = False
            if event.button == 3:
                for tower in all_towers.sprites():
                    if tower.clicked(pos[0], pos[1]):
                        print(tower.upgrade())
            if event.button == 2:
                for tower in all_towers.copy().sprites():
                    if tower.clicked(pos[0], pos[1]):
                        tower.sell()
                        board.board[(tower.rect.y - board.offset[1]) // 30][
                            (tower.rect.x - board.offset[0]) // 30] = "#"
                        all_towers.remove(tower)
    screen.fill((71, 45, 23))
    board.render()
    all_enemies.draw(screen)
    all_enemies.update()
    all_towers.draw(screen)
    for tower in all_towers.sprites():
        if current_time % 15 == 0:
            tower.attack(all_enemies.sprites())
    for enemy in all_enemies:
        if enemy.is_killed():
            all_enemies.remove(enemy)
    if enemies_left == 0 and not all_enemies.sprites():
        board.current_wave += 1
        enemies_left = board.current_wave * 5
        all_enemies = pygame.sprite.Group()
    pygame.display.flip()
    clock.tick(board.fps)
