import pygame

WALL = pygame.image.load('data/wall.png')
WALKWAY = pygame.image.load('data/walkway.jpg')
LEVEL_ENDING = pygame.image.load('data/end.jpg')
COINS = pygame.image.load('data/coins.png')
START = pygame.image.load('data/start.jpg')
TOWER = pygame.image.load('data/bigtower.png')
STOWER = pygame.image.load('data/bigtower2.png')
TOOSTOWER = pygame.image.load('data/bigtower3.png')
SOUNDICON = pygame.image.load('data/sound.png')
SOUNDICONMUTED = pygame.image.load('data/soundmute.png')
HEART = pygame.image.load('data/сердце.png')
BACKGROUND = pygame.image.load('data/background.png')
PAUSED = pygame.image.load('data/pause.png')

class Board:
    def __init__(self, width, height, board, screen):
        self.cell_size = 30
        self.screen = screen
        self.offset = (0, 60)
        pygame.display.set_mode((width * self.cell_size, height * self.cell_size + self.offset[1]))
        self.width = width * self.cell_size
        self.height = height * self.cell_size
        self.board = board
        self.play = True
        self.current_money = 10
        self.current_wave = 1
        self.hp_left = 100
        self.fps = 30
        self.enemy_rate = 1  # кол-во монстров в секунду

    def render(self):
        """
        Отрисовывает доску и верхнюю панель
        :return: None
        """
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
        self.screen.blit(COINS, (self.width - 3 * COINS.get_width() - 115, 2))
        self.screen.blit(TOWER, (self.width - self.width, 2))
        self.screen.blit(STOWER, (self.width - (self.width - 1.5 * STOWER.get_width()), 2))
        self.screen.blit(TOOSTOWER, (self.width - (self.width - 3 * STOWER.get_width()), 0))
        self.screen.blit(PAUSED, (self.width - SOUNDICON.get_width() - 74, 2))
        if self.play:
            self.screen.blit(SOUNDICON, (self.width - SOUNDICON.get_width() - 4, 2))
        else:
            self.screen.blit(SOUNDICONMUTED, (self.width - SOUNDICON.get_width() - 4, 2))
        self.screen.blit(HEART, (self.width - 400, 0))
        self.screen.blit(BACKGROUND, (0, 0))
        font = pygame.font.SysFont("comicsansms", 20)
        text = font.render("5", 1, (100, 255, 100))
        self.screen.blit(text, (self.width - self.width + 14, 30))
        text = font.render("10", 1, (100, 255, 100))
        self.screen.blit(text, (69, 30))
        text = font.render("20", 1, (100, 255, 100))
        self.screen.blit(text, (self.width - (self.width - 3.2 * STOWER.get_width()) - 1, 30))
        # TO MAKE NORMAL
        wavefont = pygame.font.SysFont("comicsansms", 26)
        wave_text = wavefont.render('ВОЛНА', 1, (255, 0, 0))
        self.screen.blit(wave_text, (self.width - 340, 0))
        l = (5 - len(str(self.current_wave))) // 2
        self.retwave = ' ' * int(l) + str(self.current_wave) + ' ' * int(l)
        wavenum_text = font.render(str(self.retwave), 1, (255, 0, 0))
        self.screen.blit(wavenum_text, (self.width - 310, 30))
        l1 = (5 - len(str(self.current_money))) / 2
        if self.current_money == 10:
            self.retmoney = '   ' * int(l1) + str(self.current_money) + ' ' * int(l1)
        else:
            self.retmoney = '  ' * int(l1) + str(self.current_money) + ' ' * int(l1)
        moneytext = font.render(str(self.retmoney), 1, (100, 255, 100))
        self.screen.blit(moneytext, (self.width - 3 * COINS.get_width() - 127, 32))
        l2 = (3 - len(str(self.hp_left))) / 2
        if len(str(self.hp_left)) != 1:
            self.hp = ' ' * int(l2) + str(self.hp_left) + ' ' * int(l2)
        else:
            self.hp = '  ' * int(l2) + str(self.hp_left) + ' ' * int(l2)
        hp_text = font.render(str(self.hp), 1, (100, 255, 100))
        self.screen.blit(hp_text, (self.width - 398, 30))

    def clicked(self, x, y):
        """
        Проверяет, был ли клик в область доски
        :param x: int
        :param y: int
        :return: None
        """
        if self.offset[0] <= x <= self.offset[0] + self.width:
            if self.offset[1] <= y <= self.offset[1] + self.height:
                return True
        return False
