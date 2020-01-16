import pygame

pygame.init()

LEVELSELECTIONWINDOW = pygame.image.load("data/startdisplay.png")


class LevelSelector:
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 600))
        self.running = True
        self.started = False
        self.level_chosen = "first"

    def run(self):
        self.screen.blit(LEVELSELECTIONWINDOW, (0, 0))
        pygame.mixer.music.load('sounds\maintheme.mp3')
        pygame.mixer.music.play(-1)
        pygame.display.flip()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if 330 <= pos[0] <= 540 and 163 <= pos[1] <= 225:
                        self.running = False
                        self.started = True
                        self.level_chosen = "first"
                    elif 325 <= pos[0] <= 540 and 245 <= pos[1] <= 309:
                        self.running = False
                        self.started = True
                        self.level_chosen = "second"
