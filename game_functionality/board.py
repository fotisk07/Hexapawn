import itertools
from game_functionality.constants import *
from game_functionality.square import Square
from game_functionality.piece import Piece, Pawn
from game_functionality.move import Move
import copy


class Board:
    def __init__(self):
        self.squares = [[0, 0, 0] for _ in range(ROWS)]
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        self.to_play = 'white'
        self.last_move = []
        self.captured_piece = []
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

    def __str__(self):
        string = f'{self.to_play} to play\n'
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    string += self.squares[row][col].piece.color[0]
                    string += " "
                else:
                    string += '. '

            string += '\n'

        return string

    def __repr__(self):
        """
        we will create a bit vector representation of the board.
        irst pass we encode 1 is a white piece is present, 0 if not
        Second pass we encode 1 if a black piece is present, 0 if not
        111 is white to move, 000 is black to move
        """

        bit_vector = ''

       # White pass

        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece() and self.squares[row][col].piece.color == 'white':
                    bit_vector += '1'
                else:
                    bit_vector += '0'

        # Black pass
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece() and self.squares[row][col].piece.color == 'black':
                    bit_vector += '1'
                else:
                    bit_vector += '0'

        # Player turn pass
        bit_vector += '111' if self.to_play == 'white' else '000'

        return bit_vector

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

    def move(self, move):
        initial = move.initial_square
        final = move.final_square

        piece = move.piece

        # Save last move, save piece that was captured
        self.last_move.append(move)
        self.captured_piece.append(self.squares[final.row][final.col].piece)

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # clear valid moves
        piece.clear_moves()

        # change player turn
        self.to_play = 'white' if self.to_play == 'black' else 'black'

    def undo_move(self):
        last_move = self.last_move.pop()
        captured_piece = self.captured_piece.pop()

        initial = last_move.initial_square
        final = last_move.final_square
        piece = last_move.piece

        self.squares[initial.row][initial.col].piece = piece
        self.squares[final.row][final.col].piece = captured_piece

        # change player turn
        self.to_play = 'white' if self.to_play == 'black' else 'black'

    def valid_moves(self, piece, move):
        return move in piece.moves

    def all_moves(self):
        colors = self.to_play
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

        for col in range(COLS):
            if self.squares[row][col].has_piece() and self.squares[row][col].piece.color == color:
                return True

        return False

    def check_winner(self):
        if len(self.all_moves()) == 0:
            self.winner = "white" if self.to_play == "black" else "black"

        if self.is_back_rank("white"):
            self.winner = "white"
        elif self.is_back_rank("black"):
            self.winner = "black"
