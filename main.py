import pygame

pygame.init()


class Board:
    def __init__(self, width, height, board, screen):
        self.screen = screen
        pygame.display.set_mode((width * 30, height * 30))
        self.width = width
        self.height = height
        self.board = board
        self.cell_size = 30

    def render(self):
        for elem in range(len(self.board)):
            for cell in range(len(self.board[elem])):
                x = cell * self.cell_size
                y = elem * self.cell_size
                pygame.draw.rect(self.screen, (255, 255, 255), (x, y, self.cell_size, self.cell_size), 1)


def scan_level(level_file_name):
    file = open(level_file_name + ".txt", encoding="utf-8").read().split("\n")
    file = list(map(list, file))
    return len(file[0]), len(file), file


screen = pygame.display.set_mode((600, 600))
board = Board(*scan_level("new_level"), screen)
print(board.board, board.height)
running = True
screen.fill((0, 0, 0))
board.render()
pygame.display.flip()
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
