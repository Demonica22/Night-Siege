import pygame
from enemies.enemie import Enemy

pygame.init()
WIZARD = pygame.image.load("data/wizard.png")


class Wizard(Enemy):
    def __init__(self, group, board):
        super().__init__(group, board)
        self.image = WIZARD
        self.board = board
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.board.start_pos
        self.passed_cells = set()  # множество из координат клеток, которые монстр уже прошел
        self.hp = 50
        self.max_hp = self.hp
        self.speed = 90 // self.board.fps
        self.reward = 1
        self.damage = 2  # Урон по крепости
