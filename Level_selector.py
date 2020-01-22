import pygame

pygame.init()

LEVELSELECTIONWINDOW = pygame.image.load("data/level_selected.png")


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
                if event.type == pygame.KEYDOWN:
                    if event.key == 27:
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if 32 <= pos[0] <= 288 and 204 <= pos[1] <= 450:
                        self.running = False
                        self.started = True
                        self.level_chosen = "first"
                    elif 320 <= pos[0] <= 566 and 205 <= pos[1] <= 455:
                        self.running = False
                        self.started = True
                        self.level_chosen = "second"
