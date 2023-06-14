
class Stats():
    def __init__(self, game, AI1, AI2=None):
        AI2 = AI1 if AI2 is None else AI2
        self.game = game
        self.ai1 = AI1()
        self.ai2 = AI2()
        self.wins = []  # 0 if black wins, 1 if white wins

    def play_games(self, N):
        print("Starting to play games...")


        for i in range(N):
            game = self.game.Game()
            board = game.board

            while not board.winner:
                if game.next_player == "white":
                    move = self.ai1.get_move(board=board, color=game.next_player)
                    board.move(move.piece, move)
                else:
                    move = self.ai2.get_move(board=board, color=game.next_player)
                    board.move(move.piece, move)

                board.check_winner(game.next_player)
                game.next_turn()

            if board.winner == "black":
                self.wins.append(0)
            else:
                self.wins.append(1)


        print("Finished playing games.")

    def win_percentage(self):
        print('This was a battle between {} and {}'.format(
            self.ai1.name, self.ai2.name))
        print('The win percentage for {} was {}%'.format(
            self.ai1.name, 100*sum(self.wins)/len(self.wins)))
