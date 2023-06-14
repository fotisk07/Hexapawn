from game_functionality import game
from analysis import stats
from ai import AI
import two_players


stats = stats.Stats(game, AI)
stats.play_games(2)
stats.win_percentage()

# play = two_players.TwoPlayers()
# play.mainloop()
