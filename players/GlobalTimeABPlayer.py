"""
MiniMax Player with AlphaBeta pruning and global time
"""
import time

from players.AbstractPlayer import AbstractPlayer
from players import AlphabetaPlayer


# TODO: you can import more modules, if needed


class Player(AlphabetaPlayer.Player):

    def __init__(self, game_time, penalty_score):
        super().__init__(game_time, penalty_score)
        self.game_time_limit = game_time
        self.long_step = None

    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        eps = 1e-2
        max_depth = float('inf')
        if not self.long_step:
            self.long_step = self.game_time_limit * 0.9 / min(self.state.size)
        if self.state.total_steps < min(self.state.size) * 2:
            my_time = self.long_step
        elif self.game_time_limit > 0.84:
            my_time = (self.game_time_limit * (1 - eps)) / 2
        elif self.game_time_limit > 0.04:
            my_time = 4e-2
        else:
            my_time = 2e-3

        cur_turn_time = min(my_time, time_limit)
        start = time.time()
        ret_val = self.make_move_aux(cur_turn_time, players_score, max_depth, set_timer=False, eps=0.6)
        end = time.time()
        print(f'Global timer: {self.game_time_limit}, turn time:{cur_turn_time}, actual time{(end - start)}')
        self.game_time_limit -= (end - start)
        return ret_val
