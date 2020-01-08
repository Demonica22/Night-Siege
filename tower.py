import pygame

pygame.init()

TOWER = pygame.image.load("data/башня.jpg")

class Tower(pygame.sprite.Sprite):
    def __init__(self, group, board):
        self.image = TOWER
        super().__init__(group)
        self.board = board
        self.rect = self.image.get_rect()

    def clickm(self, coords):
        self.rect.x, self.rect.y = coords
