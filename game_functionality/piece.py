import os


class Piece:
    def __init__(self, name, color, texture, texture_rect=None):
        self.name = name
        self.color = color
        self.texture = texture
        self.moves = []
        self.moved = False
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self):
        self.texture = os.path.join(f'assets/{self.color}_{self.name}.png')

    def add_moves(self, move):
        self.moves.append(move)
    def clear_moves(self):
        self.moves = []


class Pawn(Piece):

    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        super().__init__('pawn', color, 'pawn.png')
