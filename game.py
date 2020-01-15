import pygame
from enemies import Zombie, Wizard, Warrior
from tower import IceTower, FireTower, PlantTower
from board import Board
from level_scaner import scan_level
import random

DIEDWINDOW = pygame.image.load('data/diedwindow.png')


class Game:
    def __init__(self, current_level="first"):
        self.screen = pygame.display.set_mode((600, 600))
        self.board = Board(*scan_level(current_level), self.screen)
        self.running = True  # идет ли игра
        self.stoped = False  # была ли остановлена игра (проигрыш)
        self.hand = False  # занята ли рука ( после покупки башни кладутся в руку)
        self.showing_range_tower = False  # отображает ли одна из бишен свою дальность атаки
        self.paused = False
        self.current_level = current_level
        self.all_enemies = pygame.sprite.Group()
        self.all_towers = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.current_time = 0
        self.enemies_left = self.board.current_wave * 5
        self.enemies_delta_hp = 0
        self.pause_time = 300  # время между волнами

    def restart(self):
        """
        Обновляет все значения для новой игры.
        :return: None
        """
        self.screen = pygame.display.set_mode((600, 600))
        self.board = Board(*scan_level(self.current_level), self.screen)
        self.running = True  # идет ли игра
        self.stoped = False  # была ли остановлена игра (проигрыш)
        self.hand = False  # занята ли рука ( после покупки башни кладутся в руку)
        self.showing_range_tower = False  # отображает ли одна из бишен свою дальность атаки
        self.paused = False
        self.all_enemies = pygame.sprite.Group()
        self.all_towers = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.current_time = 0
        self.enemies_delta_hp = 0
        self.pause_time = 300  # время между волнами
        pygame.mixer.music.load('sounds\soundtrack.mp3')
        pygame.mixer.music.play(-1)
        self.screen.fill((71, 45, 23))
        self.enemies_left = self.board.current_wave * 5
        self.board.render()
        pygame.display.flip()

    def draw_die_win(self):
        """
        Рисует экран смерти.
        :return:
        """
        self.screen.blit(DIEDWINDOW, (0, 0))

    def run(self):
        pygame.mixer.music.load('sounds\soundtrack.mp3')
        pygame.mixer.music.play(-1)
        self.screen.fill((71, 45, 23))
        self.enemies_left = self.board.current_wave * 5
        self.board.render()
        pygame.display.flip()
        while self.running:
            if not self.stoped and not self.paused:
                self.current_time += 1
                if self.pause_time == 0:
                    if self.enemies_left != 0 and self.current_time % (self.board.fps // self.board.enemy_rate) == 0:
                        self.enemies_left -= 1
                        if self.board.current_wave <= 5:
                            enemy = Zombie(self.all_enemies, self.board)
                            enemy.hp += self.enemies_delta_hp
                            enemy.max_hp = enemy.hp
                        elif 3 < self.board.current_wave <= 10:
                            self.board.enemy_rate = 2
                            enemy = random.choice([1, 2])
                            if enemy == 1:
                                enemy = Zombie(self.all_enemies, self.board)
                            else:
                                enemy = Wizard(self.all_enemies, self.board)
                            enemy.hp += self.enemies_delta_hp
                            enemy.hp *= 3
                            enemy.max_hp = enemy.hp
                        else:
                            self.board.enemy_rate = 3
                            enemy = random.choice([1, 2, 3])
                            if enemy == 1:
                                enemy = Zombie(self.all_enemies, self.board)
                            elif enemy == 2:
                                enemy = Wizard(self.all_enemies, self.board)
                            else:
                                enemy = Warrior(self.all_enemies, self.board)
                            enemy.hp += self.enemies_delta_hp
                            enemy.hp *= 5
                            enemy.max_hp = enemy.hp
                        if self.board.current_wave >= 20:
                            enemy.hp *= 10
                            enemy.max_hp = enemy.hp
                else:
                    self.pause_time -= 1
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEMOTION:
                        pos = event.pos
                        for tower in self.all_towers:
                            if tower.clicked(pos[0], pos[1]):
                                print(1)
                                info_screen = pygame.Surface((30, 50))
                                self.screen.blit(info_screen, pos)
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = event.pos
                        if event.button == 1:
                            if self.showing_range_tower:
                                self.showing_range_tower.is_clicked = False
                            if 0 <= pos[0] <= 40 and 0 <= pos[1] <= 40:
                                if not self.hand and self.board.current_money >= 5:
                                    self.board.current_money -= 5
                                    self.hand = "fire"
                                elif self.hand == "fire":
                                    self.board.current_money += 5
                                    self.hand = False
                            elif 60 <= pos[0] <= 100 and 0 <= pos[1] <= 40:
                                if not self.hand and self.board.current_money >= 10:
                                    self.board.current_money -= 10
                                    self.hand = "ice"
                                elif self.hand == "ice":
                                    self.board.current_money += 10
                                    self.hand = False
                            elif 120 <= pos[0] <= 160 and 0 <= pos[1] <= 40:
                                if not self.hand and self.board.current_money >= 20:
                                    self.board.current_money -= 20
                                    self.hand = "plant"
                                elif self.hand == "plant":
                                    self.board.current_money += 20
                                    self.hand = False
                            elif 538 <= pos[0] <= 596 and 0 <= pos[1] <= 60:
                                if self.board.play:
                                    pygame.mixer.music.pause()
                                    self.board.play = False
                                else:
                                    self.board.play = True
                                    pygame.mixer.music.unpause()
                            if self.board.clicked(pos[0], pos[1]):
                                if not self.hand:
                                    for tower in self.all_towers.sprites():
                                        if tower.clicked(pos[0], pos[1]):
                                            self.showing_range_tower = tower
                                            self.showing_range_tower.is_clicked = True
                                if self.board.board[(pos[1] - self.board.offset[1]) // 30][
                                    (pos[0] - self.board.offset[0]) // 30] == '#':
                                    if self.hand:
                                        if self.hand == "fire":
                                            tower = FireTower(self.all_towers, self.board,
                                                              (pos[0] // 30 * 30, pos[1] // 30 * 30))
                                            self.board.board[(pos[1] - self.board.offset[1]) // 30][
                                                (pos[0] - self.board.offset[0]) // 30] = 'F'
                                        elif self.hand == "ice":
                                            tower = IceTower(self.all_towers, self.board,
                                                             (pos[0] // 30 * 30, pos[1] // 30 * 30))
                                            self.board.board[(pos[1] - self.board.offset[1]) // 30][
                                                (pos[0] - self.board.offset[0]) // 30] = 'I'
                                        elif self.hand == "plant":
                                            tower = PlantTower(self.all_towers, self.board,
                                                               (pos[0] // 30 * 30, pos[1] // 30 * 30))
                                            self.board.board[(pos[1] - self.board.offset[1]) // 30][
                                                (pos[0] - self.board.offset[0]) // 30] = 'P'
                                        self.hand = False
                        if event.button == 3:
                            for tower in self.all_towers.sprites():
                                if tower.clicked(pos[0], pos[1]):
                                    print(tower.upgrade())
                        if event.button == 2:
                            for tower in self.all_towers.copy().sprites():
                                if tower.clicked(pos[0], pos[1]):
                                    tower.sell()
                                    self.board.board[(tower.rect.y - self.board.offset[1]) // 30][
                                        (tower.rect.x - self.board.offset[0]) // 30] = "#"
                                    self.all_towers.remove(tower)
                                    if self.showing_range_tower == tower:
                                        self.showing_range_tower = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.paused = True
                self.screen.fill((71, 45, 23))
                self.board.render()
                self.all_towers.draw(self.screen)
                self.all_enemies.draw(self.screen)
                self.all_enemies.update()
                for tower in self.all_towers:
                    for shot in tower.shots.copy():
                        if shot.killed:
                            tower.shots.remove(shot)
                    tower.shots.draw(self.screen)
                    tower.shots.update()
                if self.showing_range_tower:
                    self.showing_range_tower.draw_range()
                for tower in self.all_towers.sprites():
                    if self.current_time % 15 == 0:
                        tower.attack(self.all_enemies.sprites())
                for enemy in self.all_enemies:
                    if enemy.is_killed():
                        self.all_enemies.remove(enemy)
                if self.enemies_left == 0 and not self.all_enemies.sprites():
                    self.pause_time = 300
                    self.board.current_wave += 1
                    self.enemies_delta_hp += 5
                    self.enemies_left = self.board.current_wave * 5
                    self.all_enemies = pygame.sprite.Group()
                if self.board.hp_left <= 0:
                    self.stoped = True
                pygame.display.flip()
                self.clock.tick(self.board.fps)
            elif self.stoped:
                self.draw_die_win()
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.restart()
            elif self.paused:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.paused = False
                    if event.type == pygame.QUIT:
                        self.running = False
