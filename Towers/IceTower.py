import pygame
from Towers.tower import Tower
from shot import Shot

pygame.init()

class IceTower(Tower):
    def __init__(self, group, board, coords):
        super().__init__(group, board, coords)
        self.level = 1
        self.images = [pygame.image.load("data/icetower" + str(n) + ".png").convert_alpha() for n in range(1, 4)]
        # Список изображений башен по уровням
        self.name = "Ледяная башня"
        self.image = self.images[self.level - 1]
        self.range = 2
        self.power = 2
        self.board = board
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
        self.upgrade_cost = [10, 50, 150]  # [level1, level2, level3]
        self.sell_cost = [9, 50, 200]  # [level1, level2, level3]

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
                self.range += 1
                self.image = self.images[self.level - 1]
                self.board.board[(self.rect.y - self.board.offset[1]) // 30][
                    (self.rect.x - self.board.offset[0]) // 30] = \
                    "I" + str(self.level)
                return "UPGRADED"
            return "Not enough money"
        return "max level"

    def attack(self, enemies):
        if enemies:
            for target in enemies.copy():
                if self.rect.x - self.range * self.board.cell_size <= target.rect.x <= self.rect.x + \
                        self.range * self.board.cell_size and \
                        self.rect.y - self.range * self.board.cell_size <= target.rect.y <= self.rect.y + \
                        self.range * self.board.cell_size:
                    if not target.slowed:
                        target.slowed = True
                        target.speed //= 2
                        if target.speed == 0:
                            target.speed = 1
                    shot = Shot(self.shots, self.board,
                                (self.rect.x + self.image.get_width() // 2, self.rect.y + self.image.get_height() // 4),
                                2,
                                self.power, target)
                    if self.level != 3:
                        break
                else:
                    enemies.remove(target)

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
