
class Move:

    def __init__(self, initial_square, final_square):
        self.initial_square = initial_square
        self.final_square = final_square
        self.piece = initial_square.piece

    def __str__(self):
        s = ''
        s += f'({self.initial.col}, {self.initial.row})'
        s += f' -> ({self.final.col}, {self.final.row})'
        return s


    def __eq__(self, other):
        return self.initial_square == other.initial_square and self.final_square == other.final_square
