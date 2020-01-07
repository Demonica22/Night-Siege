import pygame

pygame.init()

MONSTER = pygame.image.load("data/monster.jpg")


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, board):
        self.image = MONSTER
        super().__init__(group)
        self.board = board
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.board.start_pos[0] * 30, self.board.start_pos[1] * 30

    def update(self):
        if self.rect.x + 1 < len(self.board.board[0]):
            if self.board.board[self.rect.y][self.rect.x + 1] == "0":
                self.rect.move(30, 0)
                self.rect.x += 30
        elif self.rect.y + 1 < len(self.board.board):
            if self.board.board[self.rect.y + 1][self.rect.x] == "0":
                self.rect.move(0, 30)
                self.rect.y += 30

    def draw(self):
        self.board.screen.blit(self.image, (self.rect.x, self.rect.y))
