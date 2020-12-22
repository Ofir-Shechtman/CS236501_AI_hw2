"""
MiniMax Player with AlphaBeta pruning
"""
from players.MinimaxPlayer import AlgoPlayer
from SearchAlgos import AlphaBeta



class Player(AlgoPlayer):
    def __init__(self, game_time, penalty_score):
        alpha_beta = AlphaBeta(self.utility, self.succ, self.make_move, self.goal)
        super().__init__(game_time, penalty_score, alpha_beta) # keep the inheritance of the parent's (AbstractPlayer) __init__()


