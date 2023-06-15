import json
from game_functionality import move, board
from game_functionality.constants import *
import copy


class Generator:
    """
    Generator class

    This class is responsible for creating data to learn from past games.
    """

    def __init__(self):
        self.data = {}

    def minimax(self, board, isMaximizing=True):
        board.check_winner()

        if board.winner != None:
            if board.winner == 'white':
                board.winner = None
                return MAXVAL
            else:
                board.winner = None
                return MINVAL

        if isMaximizing:
            bestScore = MINVAL
            for candidate_move in board.all_moves():
                board.move(candidate_move)
                bestScore = max(bestScore, self.minimax(
                    board, False))

                board.undo_move()

            return bestScore

        else:
            bestScore = MAXVAL
            for candidate_move in board.all_moves():
                board.move(candidate_move)
                bestScore = min(bestScore, self.minimax(
                    board, True))
                board.undo_move()

            return bestScore

    def getBestMove(self, board):
        bestMove = None
        bestScore = STARTMAXVAL
        if board.to_play == 'white':
            bestScore = STARTMINVAL

        for candidate_move in board.all_moves():
            board.move(candidate_move)
            score = self.minimax(board, board.to_play == 'white')
            board.undo_move()

            if board.to_play == 'white':
                if score > bestScore:
                    bestScore = score
                    bestMove = candidate_move
            else:
                if score < bestScore:
                    bestScore = score
                    bestMove = candidate_move

        return bestMove, bestScore

    def generate_data(self, board):
        """
        Generates a dictionary with all positions and the best move associated with it.

        key : Board
        value: [best move, score]
        """
        if board.check_winner():
            return
        else:
            bestMove, bestScore = self.getBestMove(board)
            self.data[board.__repr__()] = [bestMove.__repr__(), bestScore]

            for candidate_move in board.all_moves():
                next_board = copy.deepcopy(board)
                next_board.move(candidate_move)
                self.generate_data(next_board)


if __name__ == "__main__":
    # generator = Generator()
    # board = board.Board()
    # generator.generate_data(board)
    # # count the number of 1 in bestScore in generator.data[]
    # for key, values in generator.data.items():
    #     if values[0] == 'None':
    #         print(key)
    pass
