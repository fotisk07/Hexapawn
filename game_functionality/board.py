import itertools
from constants import *
from square import Square
from piece import Piece, Pawn
from move import Move


class Board:
    def __init__(self):
        self.squares = [[0, 0, 0] for _ in range(ROWS)]
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        self.last_move = None
        self.winner = None

    def _create(self):
        self.squares = [[0, 0, 0] for _ in range(ROWS)]
        for row, col in itertools.product(range(ROWS), range(COLS)):
            self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn = 2 if color == 'white' else 0

        # Pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

    def calc_moves(self, piece, row, col):
        '''
        Calculate all possible moves for a given piece on a given square
        '''
        def pawn_moves():

            # 1 square forward
            if Square.in_range(row + piece.dir) and self.squares[row + piece.dir][col].isempty():
                initial = self.squares[row][col]
                final = self.squares[row + piece.dir][col]
                piece.add_moves(Move(initial, final))

            # Capture
            if Square.in_range(row + piece.dir) and Square.in_range(col + 1) and self.squares[row + piece.dir][col + 1].has_rival(piece.color):
                initial = self.squares[row][col]
                final = self.squares[row + piece.dir][col + 1]
                piece.add_moves(Move(initial, final))

            if Square.in_range(row + piece.dir) and Square.in_range(col - 1) and self.squares[row + piece.dir][col - 1].has_rival(piece.color):
                initial = self.squares[row][col]
                final = self.squares[row + piece.dir][col - 1]
                piece.add_moves(Move(initial, final))

        if isinstance(piece, Pawn):
            pawn_moves()

    def move(self, piece, move):
        initial = move.initial_square
        final = move.final_square

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # clear valid moves
        piece.clear_moves()

        # Set last move
        self.last_move = move

    def valid_moves(self, piece, move):
        return move in piece.moves

    def all_moves(self, colors):
        moves = []
        for row, col in itertools.product(range(ROWS), range(COLS)):
            if self.squares[row][col].has_team_piece(colors):
                piece = self.squares[row][col].piece
                self.calc_moves(piece, row, col)
                moves += piece.moves
                piece.clear_moves()
        return moves

    def is_back_rank(self, color):
        # Check if a piece of a given color has reached the back rank
        row = 0 if color == 'white' else 2

        return any(
            self.squares[row][col].has_piece()
            and self.squares[row][col].piece.color == color
            for col in range(COLS)
        )

    def check_winner(self):
        if not len(self.all_moves("white")) or not len(self.all_moves("black")):
            self.winner = "black" if not len(self.all_moves("white")) else "white"

        if self.is_back_rank("white"):
            self.winner = "white"
        elif self.is_back_rank("black"):
            self.winner = "black"