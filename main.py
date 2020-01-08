import pygame
from enemies import Enemy
from tower import Tower, TowerStrong, TowerLite
from board import Board

pygame.init()


def scan_level(level_file_name):
    file = open(level_file_name + ".txt", encoding="utf-8").read().split("\n")
    file = list(map(list, file[:-1]))
    return len(file[0]), len(file), file


screen = pygame.display.set_mode((600, 600))
board = Board(*scan_level("new_level"), screen)
running = True
screen.fill((0, 0, 0))
board.render()
all_enemies = pygame.sprite.Group()
all_towers = pygame.sprite.Group()
clock = pygame.time.Clock()
pygame.display.flip()
current_time = 0
enemies_left = board.current_wave * 5
tower1 = False
tower2 = False
while running:
    current_time += 0.5
    if enemies_left != 0 and current_time % 6 == 0:
        enemies_left -= 1
        enemy = Enemy(all_enemies, board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if not any([tower1, tower2]):
                if 0 <= pos[0] <= 40 and 0 <= pos[1] <= 40 and board.current_money >= 5:
                    board.current_money -= 5
                    tower1 = True
                elif 60 <= pos[0] <= 100 and 0 <= pos[1] <= 40 and board.current_money >= 10:
                    board.current_money -= 10
                    tower2 = True
            if board.clicked(pos[0], pos[1]) and \
                    board.board[(pos[1] - board.offset[1]) // 30][(pos[0] - board.offset[0]) // 30] == '#':
                if tower1:
                    tower = Tower(all_towers, board, (pos[0] // 30 * 30, pos[1] // 30 * 30))
                    tower1 = False
                    board.board[(pos[1] - board.offset[1]) // 30][(pos[0] - board.offset[0]) // 30] = '1'
                elif tower2:
                    tower = TowerStrong(all_towers, board, (pos[0] // 30 * 30, pos[1] // 30 * 30))
                    tower2 = False
                    board.board[(pos[1] - board.offset[1]) // 30][(pos[0] - board.offset[0]) // 30] = '2'
    screen.fill((0, 0, 0))
    board.render()
    all_enemies.draw(screen)
    all_enemies.update()
    all_towers.draw(screen)
    for tower in all_towers.sprites():
        tower.attack(all_enemies.sprites())
    for enemy in all_enemies:
        if enemy.is_killed():
            all_enemies.remove(enemy)
    if enemies_left == 0 and not all_enemies.sprites():
        board.current_wave += 1
        enemies_left = board.current_wave * 5
        all_enemies = pygame.sprite.Group()
    pygame.display.flip()
    clock.tick(2)
