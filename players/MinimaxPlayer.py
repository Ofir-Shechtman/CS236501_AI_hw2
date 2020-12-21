"""
MiniMax Player
"""
import threading
import _thread as thread
import time

from players.AbstractPlayer import AbstractPlayer, State
from SearchAlgos import MiniMax


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time,
                                penalty_score)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        self.search_algorithm = MiniMax(self.utility, self.succ, self.make_move, self.goal)