import pygame
from Towers.tower import Tower
from shot import Shot

pygame.init()


class FireTower(Tower):
    def __init__(self, group, board, coords):
        super().__init__(group, board, coords)
        self.level = 1
        self.images = [pygame.image.load("data/firetower" + str(n) + ".png").convert_alpha() for n in range(1, 4)]
        # Список изображений башен по уровням
        self.image = self.images[self.level - 1]
        self.name = "Огненная башня"
        self.board = board
        self.range = 1
        self.power = 5
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
        self.upgrade_cost = [5, 30, 50]  # [level1, level2, level3]
        self.sell_cost = [4, 30, 50]  # [level1, level2, level3]

    def upgrade(self):
        """
        Функция првоеряет, может ли быть башня улучшена, если может то улучшает и изменяет board.current_money,
        self.level, self.power
        :return: str ( результат)
        """
        if self.level < 3:
            if self.board.current_money >= self.upgrade_cost[self.level]:
                self.board.current_money -= self.upgrade_cost[self.level]
                self.level += 1
                self.image = self.images[self.level - 1]
                self.power *= 2
                self.board.board[(self.rect.y - self.board.offset[1]) // 30][
                    (self.rect.x - self.board.offset[0]) // 30] = \
                    "F" + str(self.level)
                return "UPGRADED"
            return "Not enough money"
        return "max level"

    def clicked(self, x, y):
        """
        Был ли клик на Башню
        :param x: int
        :param y: int
        :return: bool
        """
        if self.rect.x <= x <= self.rect.x + self.image.get_width():
            if self.rect.y <= y <= self.rect.y + self.image.get_height():
                return True
        return False

    def sell(self):
        self.board.current_money += self.sell_cost[self.level - 1]
