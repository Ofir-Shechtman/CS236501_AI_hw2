"""
MiniMax Player with AlphaBeta pruning with heavy heuristic
"""
from players import AlphabetaPlayer


# TODO: you can import more modules, if needed


class Player(AlphabetaPlayer.Player):
    def __init__(self, game_time, penalty_score):
        super().__init__(game_time, penalty_score)
        # TODO: initialize more fields, if needed, and the AlphaBeta algorithm from SearchAlgos.py

    def make_move(self, time_limit, players_score):
        return self.make_move_aux(time_limit, players_score, 2)

