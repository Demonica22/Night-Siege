import pygame

pygame.init()

MONSTER = pygame.image.load("data/monster.jpg")
ZOMBIE = pygame.image.load("data/zombie.png")
WIZARD = pygame.image.load("data/wizard.png")
WARRIOR = pygame.image.load("data/warrior.png")


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, board):
        self.image = MONSTER
        super().__init__(group)
        self.board = board
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.board.start_pos
        self.passed_cells = set()  # множество из координат клеток, которые монстр уже прошел
        self.hp = 5
        self.speed = 30
        self.moving = False  # двигается ли монстр
        self.reward = 1
        self.turned = "right"  # направление взгляда монстра

    def update(self):
        """
        Проверяет возможность движения монстра в любом из 4 направлений, учитывая невозможность пути в клетку,
        в которой монстр уже был.
        :return: None
        """
        if not self.moving:
            if self.rect.x // 30 + 1 < len(self.board.board[0]) and \
                    self.board.board[(self.rect.y - self.board.offset[1]) // 30][self.rect.x // 30 + 1] == "0" and not \
                    ((self.rect.y - self.board.offset[1]) // 30, self.rect.x // 30 + 1) in self.passed_cells:
                self.moving = "right"
                self.rect.x += self.speed
            elif (self.rect.y - self.board.offset[1]) // 30 + 1 < len(self.board.board) and \
                    self.board.board[(self.rect.y - self.board.offset[1]) // 30 + 1][self.rect.x // 30] == "0" and not \
                    ((self.rect.y - self.board.offset[1]) // 30 + 1, self.rect.x // 30) in self.passed_cells:
                self.moving = 'down'
                self.rect.y += self.speed
            elif 0 < self.rect.x // 30 - 1 and self.board.board[(self.rect.y - self.board.offset[1]) // 30][
                self.rect.x // 30 - 1] == "0" and not \
                    (((self.rect.y - self.board.offset[1]) // 30), self.rect.x // 30 - 1) in self.passed_cells:
                self.rect.move(-self.speed, 0)
                self.moving = "left"
                self.rect.x -= self.speed
            elif 0 < (self.rect.y - self.board.offset[1]) // 30 - 1 and \
                    self.board.board[(self.rect.y - self.board.offset[1]) // 30 - 1][self.rect.x // 30] == "0" and not \
                    ((self.rect.y - self.board.offset[1]) // 30 - 1, self.rect.x // 30) in self.passed_cells:
                self.moving = "up"
                self.rect.y -= self.speed
        else:
            self.passed_cells.add(((self.rect.y - self.board.offset[1]) // 30, self.rect.x // 30))
            if self.moving == "right":
                if self.rect.x % 30 != 0 or self.rect.x == 0:
                    if self.turned != "right":
                        self.turned = "right"
                        self.image = pygame.transform.flip(self.image, True, False)
                    self.rect.move(self.speed, 0)
                    self.rect.x += self.speed
                else:
                    self.moving = False
            elif self.moving == "left":
                if self.turned != "left":
                    self.turned = "left"
                    self.image = pygame.transform.flip(self.image, True, False)
                if self.rect.x % 30 != 0 or self.rect.x == 0:
                    self.rect.move(-self.speed, 0)
                    self.rect.x -= self.speed
                else:
                    self.moving = False
            elif self.moving == "up":
                if self.turned != "right":
                    self.turned = "right"
                    self.image = pygame.transform.flip(self.image, True, False)
                if self.rect.y % 30 != 0 or self.rect.y == 0:
                    self.rect.move(0, - self.speed)
                    self.rect.y -= self.speed
                else:
                    self.moving = False
            else:
                if self.turned != "left":
                    self.turned = "left"
                    self.image = pygame.transform.flip(self.image, True, False)
                if self.rect.y % 30 != 0 or self.rect.y == 0:
                    self.rect.move(0, self.speed)
                    self.rect.y += self.speed
                else:
                    self.moving = False

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
            self.board.current_money += self.reward
            return True
        return False


class Zombie(Enemy):
    def __init__(self, group, board):
        super().__init__(group, board)
        self.image = ZOMBIE
        self.board = board
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.board.start_pos
        self.passed_cells = set()  # множество из координат клеток, которые монстр уже прошел
        self.hp = 40
        self.speed = 60 // self.board.fps
        self.reward = 1


class Wizard(Enemy):
    def __init__(self, group, board):
        super().__init__(group, board)
        self.image = WIZARD
        self.board = board
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.board.start_pos
        self.passed_cells = set()  # множество из координат клеток, которые монстр уже прошел
        self.hp = 30
        self.speed = 90 // self.board.fps
        self.reward = 5


class Warrior(Enemy):
    def __init__(self, group, board):
        super().__init__(group, board)
        self.image = WARRIOR
        self.board = board
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.board.start_pos
        self.passed_cells = set()  # множество из координат клеток, которые монстр уже прошел
        self.hp = 100
        self.speed = 30 // self.board.fps
        self.reward = 15
