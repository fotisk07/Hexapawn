
class Move:

    def __init__(self, initial_square, final_square):
        self.initial_square = initial_square
        self.final_square = final_square
        self.piece = initial_square.piece

    def __str__(self):
        s = self.piece.color + ' '
        s += f'({self.initial_square.col}, {self.initial_square.row})'
        s += f' -> ({self.final_square.col}, {self.final_square.row})'
        return s

    def __repr__(self):
        color = self.piece.color
        init_coord = self.initial_square.single_coord()
        final_coord = self.final_square.single_coord()

        list = [0, 0, 0] if color == 'white' else [1, 1, 1]

        list += ['1' if init_coord == i else '0' for i in range(9)]
        list += ['1' if final_coord == i else '0' for i in range(9)]

        return ''.join([str(i) for i in list])

    def __eq__(self, other):
        return self.initial_square == other.initial_square and self.final_square == other.final_square
