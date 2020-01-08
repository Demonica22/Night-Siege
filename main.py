import pygame
from enemies import Enemy
from tower import Tower, TowerStrong, TowerLite
pygame.init()

WALL = pygame.image.load('data/wall.png')
WALKWAY = pygame.image.load('data/walkway.jpg')
LEVEL_ENDING = pygame.image.load('data/end.jpg')
COINS = pygame.image.load('data/coins.png')
START = pygame.image.load('data/start.jpg')
TOWER = pygame.image.load('data/BigTower.jpg')
STOWER = pygame.image.load('data/bigstrongtower.jpg')


class Board:
    def __init__(self, width, height, board, screen):
        self.cell_size = 30
        self.screen = screen
        self.offset = (0, 60)
        pygame.display.set_mode((width * 30, height * 30 + self.offset[1]))
        self.width = width * self.cell_size
        self.height = height * self.cell_size
        self.board = board
        self.current_money = 13

    def render(self):
        for elem in range(len(self.board)):
            for cell in range(len(self.board[elem])):
                x = cell * self.cell_size
                y = self.offset[1] + elem * self.cell_size
                if self.board[elem][cell] == "#":
                    self.screen.blit(WALL, (x, y))
                elif self.board[elem][cell] == "0":
                    self.screen.blit(WALKWAY, (x, y))
                elif self.board[elem][cell] == "X":
                    self.screen.blit(LEVEL_ENDING, (x, y))
                elif self.board[elem][cell] == "@":
                    self.screen.blit(START, (x, y))
                    self.start_pos = (x, y)
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.cell_size, self.cell_size), 1)
        self.screen.blit(COINS, (self.width - COINS.get_width(), 0))
        self.screen.blit(TOWER, (0, 0))
        self.screen.blit(STOWER, (60, 0))
        font = pygame.font.Font(None, 30)
        text = font.render("5", 1, (100, 255, 100))
        screen.blit(text, (15, 40))
        textstrong = font.render("10", 1, (100, 255, 100))
        screen.blit(textstrong, (67, 40))
        moneytext = font.render(str(self.current_money), 1, (100, 255, 100))
        screen.blit(moneytext, (self.width - (COINS.get_width() // 1.2), 40))


def scan_level(level_file_name):
    file = open(level_file_name + ".txt", encoding="utf-8").read().split("\n")
    file = list(map(list, file[:-1]))
    return len(file[0]), len(file), file


screen = pygame.display.set_mode((600, 600))
board = Board(*scan_level("new_level"), screen)
running = True
screen.fill((0, 0, 0))
board.render()
all_enemies = pygame.sprite.Group()
enemy = Enemy(all_enemies, board)
all_towers = pygame.sprite.Group()
clock = pygame.time.Clock()
pygame.display.flip()
current_wave = 1
current_time = 0
tower1 = False
tower2 = False
while running:
    current_time += 0.5
    if len(all_enemies) < current_wave * 5 and current_time % 20 == 0:
        enemy = Enemy(all_enemies, board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if 0 <= pos[0] <= 40 and 0 <= pos[1] <= 40 and board.current_money >= 5 and not tower1 and not tower2:
                board.current_money -= 5
                tower1 = True
            elif 60 <= pos[0] <= 100 and 0 <= pos[1] <= 40 and board.current_money >= 10 and not tower1 and not tower2:
                board.current_money -= 10
                tower2 = True
            if board.offset[1] <= pos[1] <= board.offset[1] + len(board.board) * board.cell_size and \
                    0 <= pos[0] <= len(board.board[0]) * board.cell_size and \
                    board.board[(pos[1] - board.offset[1]) // 30][(pos[0] - board.offset[0]) // 30] == '#':
                if tower1:
                    tower = Tower(all_towers, board, (pos[0] // 30 * 30, pos[1] // 30 * 30))
                elif tower2:
                    tower = TowerStrong(all_towers, board, (pos[0] // 30 * 30, pos[1] // 30 * 30))
                all_towers.add(tower)
                board.board[(pos[1] - board.offset[1]) // 30][(pos[0] - board.offset[0]) // 30] = '1'
                tower1 = False
    screen.fill((0, 0, 0))
    board.render()
    all_enemies.draw(screen)
    all_enemies.update()
    all_towers.draw(screen)
    for enem in all_enemies:
        if enem.is_killed():
            all_enemies.remove(enem)
    if all([enem.is_killed() for enem in all_enemies]):
        current_wave += 1
        all_enemies = pygame.sprite.Group()
    pygame.display.flip()
    clock.tick(10)
