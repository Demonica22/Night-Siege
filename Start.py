import pygame

pygame.init()

STARTWINDOW = pygame.image.load("data/startdisplay.png")


class Start:
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 600))
        self.playing = True
        self.running = True
        self.started = False
        self.stats = False

    def run(self):
        self.screen.blit(STARTWINDOW, (0, 0))
        pygame.mixer.music.load('sounds\maintheme.mp3')
        pygame.mixer.music.play(-1)
        pygame.display.flip()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.playing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    # Проверка на клик по кнопке Start
                    if 163 <= pos[0] <= 374 and 163 <= pos[1] <= 224:
                        self.running = False
                        self.started = True
                    # Проверка на клик по кнопке Exit
                    elif 163 <= pos[0] <= 375 and 338 <= pos[1] <= 400:
                        self.running = False
                        self.playing = False
                    # Проверка на клик по кнопке Stats
                    elif 163 <= pos[0] <= 375 and 248  <= pos[1] <= 308 :
                        self.running = False
                        self.stats = True
