import pygame
from enemies.enemy import Enemy

pygame.init()
WARRIOR = pygame.image.load("data/warrior.png")


class Warrior(Enemy):
    def __init__(self, group, board):
        super().__init__(group, board)
        self.image = WARRIOR
        self.board = board
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.board.start_pos
        self.passed_cells = set()  # множество из координат клеток, которые монстр уже прошел
        self.hp = 150
        self.max_hp = self.hp
        self.speed = 30 // self.board.fps
        self.reward = 5
        self.damage = 5  # Урон по крепости
