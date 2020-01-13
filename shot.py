import pygame

RED = pygame.image.load("data/redball.png")
BLUE = pygame.image.load("data/blueball.png")
GREEN = pygame.image.load("data/greenball.png")


class Shot(pygame.sprite.Sprite):
    def __init__(self, group, board, pos, color, power, target):

        super().__init__(group)
        self.color = color
        self.board = board
        self.target = target
        self.speed = 180 // board.fps
        self.power = power
        self.image = [RED, BLUE, GREEN][self.color - 1]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.killed = False

    def update(self, *args):
        if self.rect.x != (
                self.target.rect.x + self.target.image.get_width()//2) or self.rect.y != (
                self.target.rect.y + self.target.image.get_height()//2):
            delta = False
            if self.rect.x != self.target.rect.x + self.target.image.get_width()//2:
                if abs(self.rect.x - (self.target.rect.x + self.target.image.get_width()//2)) < self.speed:
                    delta = abs(self.rect.x - (self.target.rect.x + self.target.image.get_width()//2))
                if not delta:
                    if (self.target.rect.x + self.target.image.get_width()//2) > self.rect.x:
                        self.rect.x += self.speed
                    else:
                        self.rect.x -= self.speed
                else:
                    if (self.target.rect.x + self.target.image.get_width()//2) > self.rect.x:
                        self.rect.x += delta
                    else:
                        self.rect.x -= delta
            delta = False
            if self.rect.y != (self.target.rect.y + self.target.image.get_height()//2):
                if abs(self.rect.y - (self.target.rect.y + self.target.image.get_height()//2)) < self.speed:
                    delta = abs(self.rect.y - (self.target.rect.y + self.target.image.get_height()//2))
                if not delta:
                    if (self.target.rect.y + self.target.image.get_height()//2) > self.rect.y:
                        self.rect.y += self.speed
                    else:
                        self.rect.y -= self.speed
                else:
                    if (self.target.rect.y + self.target.image.get_height()//2) > self.rect.y:
                        self.rect.y += delta
                    else:
                        self.rect.y -= delta
            self.draw(self.board.screen)
        else:
            if self.color == 2:
                if not self.target.slowed:
                    self.target.slowed = True
                    self.target.speed //= 2
                    if self.target.speed == 0:
                        self.target.speed = 1
            self.target.get_shoted(self.power)
            self.killed = True

    def draw(self, *args, **kwargs):
        pass
