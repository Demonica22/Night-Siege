import pygame
from Game import Game
from Start import Start
from Level_selector import LevelSelector
from Stats_window import Stats

pygame.init()
pygame.display.set_caption("Night Siege")
start = Start()
start.run()
if start.started:
    level_selector = LevelSelector()
    level_selector.run()
    if level_selector.started:
        game = Game(level_selector.level_chosen)
        game.run()
elif start.stats:
    stats = Stats()
    stats.run()
    while stats.running:
        pass
    start.stats = False
while start.playing:
    start = Start()
    start.run()
    if start.started:
        level_selector = LevelSelector()
        level_selector.run()
        if level_selector.started:
            game = Game(level_selector.level_chosen)
            game.run()
    elif start.stats:
        stats = Stats()
        stats.run()
        while stats.running:
            pass
        start.stats = False
