from square import Square



class AI():
    def __init__(self):
        pass


    def get_move(self, board):
        moves = board.all_moves("black")

        return moves[0]
    