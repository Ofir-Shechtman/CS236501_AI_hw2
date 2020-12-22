"""
MiniMax Player with AlphaBeta pruning with light heuristic
"""
from players import AlphabetaPlayer
from players.MinimaxPlayer import State
#TODO: you can import more modules, if needed


class Player(AlphabetaPlayer.Player):
    def __init__(self, game_time, penalty_score):
        super().__init__(game_time, penalty_score)
        #TODO: initialize more fields, if needed, and the AlphaBeta algorithm from SearchAlgos.py

    def make_move(self, time_limit, players_score):
        return self.make_move_aux(time_limit, players_score, 4)

    def utility(self, state: State, turn):
        comp1 = self.utility_component1(state, turn)
        simple = self.utility_component2(state, turn)
        w1, w3, w4 = 1, 1, 1
        return comp1 * w1 + simple * 10