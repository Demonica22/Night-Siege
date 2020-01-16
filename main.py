import pygame
from game import Game

pygame.init()
pygame.display.set_caption("TD game")
pygame.mixer.music.load('sounds\maintheme.mp3')
pygame.mixer.music.play(-1)
game = Game()
game.run()
