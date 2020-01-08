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
        self.range = 1  # дальность атаки башни
        self.power = 1

    def click(self, x, y):
        if x <= self.x + self.image.get_width() and self.x >= x:
            if y <= self.y + self.image.get_height() and self.y >= y:
                return True
        return False

    def attack(self, enemies):
        if enemies:
            for target in enemies.copy():
                if self.rect.x - self.range * self.board.cell_size <= target.rect.x <= self.rect.x + self.range * self.board.cell_size and \
                        self.rect.y - self.range * self.board.cell_size <= target.rect.y <= self.rect.y + self.range * self.board.cell_size:
                    if target.get_shoted(self.power):
                        enemies.remove(target)
                else:
                    enemies.remove(target)


class TowerLite(Tower):
    def __init__(self, group, board, coords):
        super().__init__(group, board, coords)
        self.image = TOWER
        self.board = board
        self.range = 1
        self.power = 1
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords


class TowerStrong(Tower):
    def __init__(self, group, board, coords):
        super().__init__(group, board, coords)
        self.range = 2
        self.power = 5
        self.image = TOWERS
        self.board = board
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
