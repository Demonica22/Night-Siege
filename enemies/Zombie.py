import pygame
from enemies.enemy import Enemy

pygame.init()

ZOMBIE = pygame.image.load("data/zombie.png")


class Zombie(Enemy):
    def __init__(self, group, board):
        super().__init__(group, board)
        self.image = ZOMBIE
        self.board = board
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.board.start_pos
        self.passed_cells = set()  # множество из координат клеток, которые монстр уже прошел
        self.hp = 40
        self.max_hp = self.hp
        self.speed = 60 // self.board.fps
        self.reward = 1
        self.damage = 1  # Урон по крепости
