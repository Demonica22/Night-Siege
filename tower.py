import pygame
from shot import Shot

pygame.init()


class Tower(pygame.sprite.Sprite):
    def __init__(self, group, board, coords):
        super().__init__(group)
        self.board = board
        self.range = 1  # дальность атаки башни
        self.power = 1
        self.is_clicked = False
        self.shots = pygame.sprite.Group()

    def clicked(self, x, y):
        if x <= self.x + self.image.get_width() and self.x >= x:
            if y <= self.y + self.image.get_height() and self.y >= y:
                return True
        return False

    def attack(self, enemies):
        if enemies:
            for target in enemies.copy():
                if self.rect.x - self.range * self.board.cell_size <= target.rect.x <= self.rect.x + \
                        self.range * self.board.cell_size and \
                        self.rect.y - self.range * self.board.cell_size <= target.rect.y <= self.rect.y + \
                        self.range * self.board.cell_size:
                    shot = Shot(self.shots, self.board,
                                (self.rect.x + self.image.get_width()//2, self.rect.y + self.image.get_height()//2), 1,
                                self.power, target)
                    break
                else:
                    enemies.remove(target)

    def draw_range(self):
        if self.is_clicked:
            if self.board.offset[1] > self.rect.y - (self.board.cell_size * self.range):
                delta = self.board.offset[1] - (self.rect.y - (self.board.cell_size * self.range))
            else:
                delta = 0
            pygame.draw.rect(self.board.screen, (255, 0, 0, 0.4),
                             pygame.Rect((self.rect.x - (self.board.cell_size * self.range),
                                          self.rect.y - (self.board.cell_size * self.range) + abs(delta)),
                                         (self.board.cell_size * (self.range * 2 + 1),
                                          self.board.cell_size * (self.range * 2 + 1) - abs(delta))), 1)


class FireTower(Tower):
    def __init__(self, group, board, coords):
        super().__init__(group, board, coords)
        self.level = 1
        self.images = [pygame.image.load("data/firetower" + str(n) + ".png").convert_alpha() for n in range(1, 4)]
        # Список изображений башен по уровням
        self.image = self.images[self.level - 1]
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


class IceTower(Tower):
    def __init__(self, group, board, coords):
        super().__init__(group, board, coords)
        self.level = 1
        self.images = [pygame.image.load("data/icetower" + str(n) + ".png").convert_alpha() for n in range(1, 4)]
        # Список изображений башен по уровням
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
                                (self.rect.x + self.image.get_width() // 2, self.rect.y + self.image.get_height() // 2),
                                2,
                                self.power, target)
                    shot.draw(self.board.screen)
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


class PlantTower(Tower):
    def __init__(self, group, board, coords):
        super().__init__(group, board, coords)
        self.level = 1
        self.images = [pygame.image.load("data/planttower" + str(n) + ".png").convert_alpha() for n in range(1, 4)]
        # Список изображений башен по уровням
        self.image = self.images[self.level - 1]
        self.range = 1
        self.power = 15
        self.board = board
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
        self.upgrade_cost = [20, 100, 200]  # [level1, level2, level3]
        self.sell_cost = [19, 100, 300]  # [level1, level2, level3]

    def attack(self, enemies):
        if enemies:
            for target in enemies.copy():
                if self.rect.x - self.range * self.board.cell_size <= target.rect.x <= self.rect.x + \
                        self.range * self.board.cell_size and \
                        self.rect.y - self.range * self.board.cell_size <= target.rect.y <= self.rect.y + \
                        self.range * self.board.cell_size:
                    shot = Shot(self.shots, self.board,
                                (self.rect.x + self.image.get_width() // 2, self.rect.y + self.image.get_height() // 2),
                                3,
                                self.power, target)
                    shot.draw(self.board.screen)
                else:
                    enemies.remove(target)

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
                    "P" + str(self.level)
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
