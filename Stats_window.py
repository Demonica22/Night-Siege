import pygame
from statistics_getter import get_statistics

pygame.init()

STATS_WINDOW = pygame.image.load("data/startdisplay.png")


class Stats:
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 600))
        self.running = True

    def run(self):
        stats = get_statistics()
        self.screen.blit(STATS_WINDOW, (0, 0))
        font = pygame.font.SysFont("comicsansms", 20)
        text = font.render(str(stats[0]) + " waves", 1, (0, 0, 0))
        self.screen.blit(text, (200, 90))
        text = font.render(str(stats[1]) + " waves", 1, (0, 0, 0))
        self.screen.blit(text, (200, 130))
        text = font.render(str(stats[2]) + " waves", 1, (0, 0, 0))
        self.screen.blit(text, (200, 180))
        pygame.display.flip()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == 27:
                        self.running = False
