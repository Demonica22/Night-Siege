import pygame

pygame.init()

TOWER = pygame.image.load("data/башня.jpg")
TOWERS = pygame.image.load("data/strongtower.jpg")

class Tower(pygame.sprite.Sprite):
    def __init__(self, group, board):
        self.image = TOWER
        super().__init__(group)
        self.board = board
        self.rect = self.image.get_rect()

class TowerLite(Tower):
    def __init__(self):
        self.image = TOWER
        super().__init__(group)
        self.board = board
        self.rect = self.image.get_rect()


class TowerStrong(Tower):
    def __init__(self):
        image_s = TOWERS
        super().__init__(group)
        self.board = board
        self.rect = self.image_s.get_rect()