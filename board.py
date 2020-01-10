import pygame

WALL = pygame.image.load('data/wall.png')
WALKWAY = pygame.image.load('data/walkway.jpg')
LEVEL_ENDING = pygame.image.load('data/end.jpg')
COINS = pygame.image.load('data/coins.png')
START = pygame.image.load('data/start.jpg')
TOWER = pygame.image.load('data/bigtower.png')
STOWER = pygame.image.load('data/bigtower2.png')


class Board:
    def __init__(self, width, height, board, screen):
        self.cell_size = 30
        self.screen = screen
        self.offset = (0, 60)
        pygame.display.set_mode((width * 30, height * 30 + self.offset[1]))
        self.width = width * self.cell_size
        self.height = height * self.cell_size
        self.board = board
        self.current_money = 10
        self.current_wave = 1
        self.hp_left = 100
        self.fps = 30

    def render(self):
        for elem in range(len(self.board)):
            for cell in range(len(self.board[elem])):
                x = cell * self.cell_size
                y = self.offset[1] + elem * self.cell_size
                if self.board[elem][cell] == "0":
                    self.screen.blit(WALKWAY, (x, y))
                elif self.board[elem][cell] == "X":
                    self.end_pos = (x, y)
                    self.screen.blit(LEVEL_ENDING, (x, y))
                elif self.board[elem][cell] == "@":
                    self.screen.blit(START, (x, y))
                    self.start_pos = (x, y)
                else:
                    self.screen.blit(WALL, (x, y))
                # pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.cell_size, self.cell_size), 1)
        self.screen.blit(COINS, (self.width - COINS.get_width(), 0))
        self.screen.blit(TOWER, (0, 0))
        self.screen.blit(STOWER, (60, 0))
        font = pygame.font.Font(None, 30)
        text = font.render("5", 1, (100, 255, 100))
        self.screen.blit(text, (15, 40))
        textstrong = font.render("10", 1, (100, 255, 100))
        self.screen.blit(textstrong, (67, 40))
        # TO MAKE NORMAL
        wave_text = font.render("current_wave " + str(self.current_wave), 1, (255, 0, 0))
        self.screen.blit(wave_text, (self.width - 250, 40))
        # TO MAKE NORMAL
        moneytext = font.render(str(self.current_money), 1, (100, 255, 100))
        self.screen.blit(moneytext, (self.width - (COINS.get_width() // 1.2), 40))
        # СДЕЛАТЬ НОРМАЛЬНО
        hp_text = font.render("HP " + str(self.hp_left), 1, (100, 255, 100))
        self.screen.blit(hp_text, (self.width - 400, 40))

    def clicked(self, x, y):
        if self.offset[0] <= x <= self.offset[0] + self.width:
            if self.offset[1] <= y <= self.offset[1] + self.height:
                return True
        return False
