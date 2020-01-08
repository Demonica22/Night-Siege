import pygame

pygame.init()

MONSTER = pygame.image.load("data/monster.jpg")


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, board):
        self.image = MONSTER
        super().__init__(group)
        self.board = board
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.board.start_pos
        self.passed_cells = set()  # множество из координат клеток, которые монстр уже прошел
        self.hp = 5

    def update(self):
        """
        Проверяет возможность движения монстра в любом из 4 направлений, учитывая невозможность пути в клетку,
        в которой монстр уже был.
        :return: None
        """
        self.speed = 30
        if self.rect.x // 30 + 1 < len(self.board.board[0]) and \
                self.board.board[(self.rect.y - self.board.offset[1]) // 30][self.rect.x // 30 + 1] == "0" and not \
                ((self.rect.y - self.board.offset[1]) // 30, self.rect.x // 30 + 1) in self.passed_cells:
            self.rect.move(self.speed, 0)
            self.rect.x += self.speed
            self.passed_cells.add(((self.rect.y - self.board.offset[1]) // 30, self.rect.x // 30))
        elif (self.rect.y - self.board.offset[1]) // 30 + 1 < len(self.board.board) and \
                self.board.board[(self.rect.y - self.board.offset[1]) // 30 + 1][self.rect.x // 30] == "0" and not \
                ((self.rect.y - self.board.offset[1]) // 30 + 1, self.rect.x // 30) in self.passed_cells:
            self.rect.move(0, self.speed)
            self.rect.y += self.speed
            self.passed_cells.add(((self.rect.y - self.board.offset[1]) // 30, self.rect.x // 30))
        elif 0 <= self.rect.x // 30 - 1 and self.board.board[(self.rect.y - self.board.offset[1]) // 30][
            self.rect.x // 30 - 1] == "0" and not \
                (((self.rect.y - self.board.offset[1]) // 30), self.rect.x // 30 - 1) in self.passed_cells:
            self.rect.move(-self.speed, 0)
            self.rect.x -= self.speed
            self.passed_cells.add(((self.rect.y - self.board.offset[1]) // 30, self.rect.x // 30))
        elif 0 <= (self.rect.y - self.board.offset[1]) // 30 - 1 and \
                self.board.board[(self.rect.y - self.board.offset[1]) // 30 - 1][self.rect.x // 30] == "0" and not \
                ((self.rect.y - self.board.offset[1]) // 30 - 1, self.rect.x // 30) in self.passed_cells:
            self.rect.move(0, -self.speed)
            self.rect.y -= self.speed
            self.passed_cells.add(((self.rect.y - self.board.offset[1]) // 30, self.rect.x // 30))

    def is_killed(self):
        """
        Проверка, был ли убит монстр
        :return: bool
        """
        if self.hp <= 0:
            return True
        return False

    def get_shoted(self, bullet_power):
        """
        Получение выстрела с силой bullet_power (количество отнимаемого хп) и проверка на смерть монстра
        :param bullet_power: Сила выстрела (урон по монстру)
        :return: bool
        """
        self.hp -= bullet_power
        if self.is_killed():
            self.board.current_money += 1
            return True
        return False
