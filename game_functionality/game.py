import itertools
import pygame
from constants import *

from board import Board
from dragger import Dragger
from square import Square
from ai import AI


class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.ai = AI()
        self.next_player = 'white'
        self.hover_square = None

    def show_bg(self, surface):
        for row, col in itertools.product(range(ROWS), range(COLS)):
            color = LIGHT_GREEN if (row + col) % 2 == 0 else DARK_GREEN

            rect = (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)

            pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row, col in itertools.product(range(ROWS), range(COLS)):
            if self.board.squares[row][col].has_piece():
                piece = self.board.squares[row][col].piece

                # all pieces except dragger piece
                if piece != self.dragger.piece:

                    img = pygame.image.load(piece.texture)

                    img_center = col*SQSIZE + SQSIZE//2, row*SQSIZE + SQSIZE//2
                    piece.texture_rect = img.get_rect(center=img_center)
                    surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                # color
                color = LIGHT_RED if (move.final_square.row +
                                      move.final_square.col) % 2 == 0 else DARK_RED
                # rect
                rect = (move.final_square.col*SQSIZE,
                        move.final_square.row*SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        if self.board.last_move:
            initial = self.board.last_move.initial_square
            final = self.board.last_move.final_square

            for pos in [initial, final]:
                # color
                color = GREEN1 if (
                    pos.row + pos.col) % 2 == 0 else GREEN2
                # rect
                rect = (pos.col*SQSIZE, pos.row*SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hover_square and Square.in_range(self.hover_square.row, self.hover_square.col):
            # color
            color = BLUE
            # rect
            rect = (self.hover_square.col*SQSIZE,
                    self.hover_square.row*SQSIZE, SQSIZE, SQSIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=3)

    def show_winner(self, surface, color):
        if color == "white":
            img = pygame.image.load(WHITE_WINS)
            surface.blit(img, (0, 0))
        elif color == "black":
            img = pygame.image.load(BLACK_WINS)
            surface.blit(img, (0, 0))

    # Other methods

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        if Square.in_range(row, col):
            self.hover_square = self.board.squares[row][col]

    def reset(self):
        self.__init__()
