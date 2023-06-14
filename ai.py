from game_functionality.square import Square



class AI():
    def __init__(self):
        self.name = "Random AI"


    def get_move(self, board, color="black"):
        moves = board.all_moves(color)

        return moves[0]
    