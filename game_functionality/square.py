
class Square:
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    def single_coord(self):
        return self.row * 3 + self.col


    def has_piece(self):
        return self.piece != None

    def isempty(self):
        return not self.has_piece()

    def has_rival(self, color):
        return self.has_piece() and self.piece.color != color

    def isempty_or_rival(self, color):
        return self.isempty() or self.has_rival(color)

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    @staticmethod
    def in_range(*args):
        # sourcery skip: use-any, use-next
        for arg in args:
            if arg < 0 or arg > 2:
                return False
        return True
