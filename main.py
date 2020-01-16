import pygame
from game import Game
from Start import Start

pygame.init()
pygame.display.set_caption("Night Siege")
start = Start()
start.run()
if start.started:
    game = Game()
    game.run()
