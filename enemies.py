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
        self.passed_cells = set()

    def update(self):
        if self.rect.x // 30 + 1 < len(self.board.board[0]) and \
                self.board.board[(self.rect.y - self.board.offset[1]) // 30][self.rect.x // 30 + 1] == "0" and not \
                ((self.rect.y - self.board.offset[1]) // 30 , self.rect.x // 30 + 1) in self.passed_cells:
            print("->")
            self.rect.move(30, 0)
            self.rect.x += 30
            self.passed_cells.add(((self.rect.y - self.board.offset[1]) // 30, self.rect.x // 30))
        elif (self.rect.y - self.board.offset[1]) // 30 + 1 < len(self.board.board) and \
                self.board.board[(self.rect.y - self.board.offset[1]) // 30 + 1][self.rect.x // 30] == "0" and not \
                ((self.rect.y - self.board.offset[1]) // 30 + 1, self.rect.x // 30) in self.passed_cells:
            print("|")
            self.rect.move(0, 30)
            self.rect.y += 30
            self.passed_cells.add(((self.rect.y - self.board.offset[1]) // 30, self.rect.x // 30))
        elif 0 <= self.rect.x // 30 - 1 and self.board.board[(self.rect.y - self.board.offset[1]) // 30][
            self.rect.x // 30 - 1] == "0" and not \
                (((self.rect.y - self.board.offset[1]) // 30), self.rect.x // 30 - 1) in self.passed_cells:
            print("<-")
            self.rect.move(-30, 0)
            self.rect.x -= 30
            self.passed_cells.add(((self.rect.y - self.board.offset[1]) // 30, self.rect.x // 30))
        elif 0 <= (self.rect.y - self.board.offset[1]) // 30 - 1 and \
                self.board.board[(self.rect.y - self.board.offset[1]) // 30 - 1][self.rect.x // 30] == "0" and not \
                ((self.rect.y - self.board.offset[1]) // 30 - 1, self.rect.x // 30) in self.passed_cells:
            print("^")
            self.rect.move(0, -30)
            self.rect.y -= 30
            self.passed_cells.add(((self.rect.y - self.board.offset[1]) // 30, self.rect.x // 30))
