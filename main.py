import pygame
from enemies import Enemy
from tower import Tower

pygame.init()

WALL = pygame.image.load('data/wall.png')
WALKWAY = pygame.image.load('data/walkway.jpg')
LEVEL_ENDING = pygame.image.load('data/end.jpg')
CHEST = pygame.image.load('data/shop.png')
START = pygame.image.load('data/start.jpg')


class Board:
    def __init__(self, width, height, board, screen):
        self.cell_size = 30
        self.screen = screen
        pygame.display.set_mode((width * 30, height * 30 + 60))
        self.offset = (0, 60)
        self.width = width * self.cell_size
        self.height = height * self.cell_size
        self.board = board

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
        self.screen.blit(CHEST, (self.width - CHEST.get_width(), 0))


def scan_level(level_file_name):
    file = open(level_file_name + ".txt", encoding="utf-8").read().split("\n")
    file = list(map(list, file))
    return len(file[0]), len(file), file


screen = pygame.display.set_mode((600, 600))
board = Board(*scan_level("new_level"), screen)
running = True
screen.fill((0, 0, 0))
board.render()
all_enemies = pygame.sprite.Group()
enemy = Enemy(all_enemies, board)
all_enemies.draw(screen)
all_towers = pygame.sprite.Group()
clock = pygame.time.Clock()
pygame.display.flip()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if board.board[(pos[1] - board.offset[1]) // 30][(pos[0] - board.offset[0]) // 30] == '#':
                tower = Tower(all_towers, board, (pos[0] // 30 * 30, pos[1] // 30 * 30))
                all_towers.add(tower)
    screen.fill((0, 0, 0))
    board.render()
    all_enemies.draw(screen)
    all_enemies.update()
    all_towers.draw(screen)
    pygame.display.flip()
    clock.tick(3)
