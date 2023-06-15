from game_functionality.square import Square
from generator import Generator


class AI():
    def __init__(self):
        self.name = "MiniMax"
        self.generator = Generator()

    def __repr__(self):
        return self.name


    def get_move(self, board):
        print("AI is thinking...")   
        move = self.generator.getBestMove(board)[0]
        return move
    