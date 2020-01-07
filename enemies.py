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
        self.passed_cells = []

    def update(self):
        done = False
        if self.rect.x // 30 + 1 < len(self.board.board[0]):
            if self.board.board[(self.rect.y - self.board.offset[1]) // 30][self.rect.x // 30 + 1] == "0":
                self.rect.move(1, 0)
                self.rect.x += 1
                self.passed_cells.append(((self.rect.y - self.board.offset[1]) // 30, self.rect.x // 30))
                done = True
            if 0 <= self.rect.x // 30 - 1:
                if self.board.board[(self.rect.y - self.board.offset[1]) // 30][self.rect.x // 30 - 1] == "0" and not \
                        (((self.rect.y - self.board.offset[1]) // 30), self.rect.x // 30 - 1) in self.passed_cells:
                    self.rect.move(-1, 0)
                    self.rect.x -= 1
                    self.passed_cells.append(((self.rect.y - self.board.offset[1]) // 30, self.rect.x // 30))
                    done = True
        if (self.rect.y - self.board.offset[1]) // 30 + 1 < len(self.board.board) and not done:
            if self.board.board[(self.rect.y - self.board.offset[1]) // 30 + 1][self.rect.x // 30] == "0":
                self.rect.move(0, 1)
                self.rect.y += 1
                self.passed_cells.append(((self.rect.y - self.board.offset[1]) // 30, self.rect.x // 30))
            if 0 <= (self.rect.y - self.board.offset[1]) // 30 - 1:
                if self.board.board[(self.rect.y - self.board.offset[1]) // 30 - 1][self.rect.x // 30] == "0" and not \
                        ((self.rect.y - self.board.offset[1]) // 30 - 1, self.rect.x // 30) in self.passed_cells:
                    self.rect.move(0, -1)
                    self.rect.y -= 1
                    self.passed_cells.append(((self.rect.y - self.board.offset[1]) // 30, self.rect.x // 30))
