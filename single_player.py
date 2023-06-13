import pygame
import sys

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SQSIZE
from game import Game
from square import Square
from move import Move


class two_players:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Hexapawn")
        self.game = Game()


    def mainloop(self):

        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board

        
        
        