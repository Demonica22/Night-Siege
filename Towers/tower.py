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
                                (self.rect.x + self.image.get_width() // 2, self.rect.y + self.image.get_height() // 4),
                                1,
                                self.power, target)
                    break
                else:
                    enemies.remove(target)

    def draw_info(self):
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
            info_screen = pygame.Surface([125, 60], pygame.SRCALPHA, 32)
            info_screen = info_screen.convert_alpha()
            self.info = [f"{self.name} {self.level} уровня", f"С атакой {self.power}"]
            delta_y = 10
            if self.level < 3:
                self.info.append(f"Цена улучшения {self.upgrade_cost[self.level]}")
                delta_y = 20
            font = pygame.font.SysFont("comicsansms", 10)
            delta = 0
            for line in self.info:
                info_text = font.render(line, 1, (255, 255, 255))
                info_screen.blit(info_text, (0, delta))
                delta += 10
            self.board.screen.blit(info_screen, (self.rect.x, self.rect.y - (20 + delta_y)))
