import pygame

pygame.init()

TOWER = pygame.image.load("data/башня.jpg")
TOWERS = pygame.image.load("data/strongtower.jpg")


class Tower(pygame.sprite.Sprite):
    def __init__(self, group, board, coords):
        super().__init__(group)
        self.image = TOWER
        self.rect = self.image.get_rect()
        self.board = board
        self.rect.x, self.rect.y = coords


class TowerLite(Tower):
    def __init__(self, group, board, coords):
        super().__init__(group, board, coords)
        self.image = TOWER
        self.board = board
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords


class TowerStrong(Tower):
    def __init__(self, group, board, coords):
        super().__init__(group, board, coords)
        self.image = TOWERS
        self.board = board
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
