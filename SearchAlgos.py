"""Search Algos: MiniMax, AlphaBeta
"""
import time

from utils import ALPHA_VALUE_INIT, BETA_VALUE_INIT


# TODO: you can import more modules, if needed


class SearchAlgos:
    def __init__(self, utility, succ, perform_move, goal=None):
        """The constructor for all the search algos.
        You can code these functions as you like to, 
        and use them in MiniMax and AlphaBeta algos as learned in class
        :param utility: The utility function.
        :param succ: The succesor function.
        :param perform_move: The perform move function.
        :param goal: function that check if you are in a goal state.
        """
        self.utility = utility
        self.succ = succ
        self.perform_move = perform_move
        self.goal = goal
        self._reach_end = True
        self.timer = None

    class Timer:
        def __init__(self, time_limit):
            self.time_limit = time_limit

        def reset(self):
            self.start_time = time.time()

        def timeout(self):
            return time.time() - self.start_time > self.time_limit - 1e-2

    def setup_timer(self, time_limit):
        self.timer = self.Timer(time_limit)
        self.timer.reset()


    def set_end_reason(self, flag: bool):
        self._reach_end = flag

    @property
    def end_reason(self):
        return self._reach_end

    def search(self, state, depth, maximizing_player):
        raise NotImplementedError


class MiniMax(SearchAlgos):

    def search(self, state, depth, maximizing_player):
        """Start the MiniMax algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        if self.timer.timeout():
            print(f'timeout on: {time.time()-self.timer.start_time}')
            raise TimeoutError
        turn = 1 if maximizing_player else 2
        if self.goal(state, turn):
            return self.utility(state, turn), None
        elif depth == 0:
            self.set_end_reason(False)
            return self.utility(state, turn), None
        else:
            if maximizing_player:
                max_val = float('inf') * -1
                max_direction = None
                for child in self.succ(state, 1):
                    val, _ = self.search(child, depth - 1, not maximizing_player)
                    if val > max_val:
                        max_val = val
                        max_direction = child.last_move
                return max_val, max_direction
            else:
                min_val = float('inf')
                for child in self.succ(state, 2):
                    val, _ = self.search(child, depth - 1, not maximizing_player)
                    if val < min_val:
                        min_val = val
                return min_val, None


class AlphaBeta(SearchAlgos):

    def search(self, state, depth, maximizing_player, alpha=ALPHA_VALUE_INIT, beta=BETA_VALUE_INIT):
        """Start the AlphaBeta algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :param alpha: alpha value
        :param: beta: beta value
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        if self.timer.timeout():
            print(f'timeout on: {time.time()-self.timer.start_time}')
            raise TimeoutError
        turn = 1 if maximizing_player else 2
        if self.goal(state, turn):
            return self.utility(state, turn), None
        elif depth == 0:
            self.set_end_reason(False)
            return self.utility(state, turn), None
        else:
            if maximizing_player:
                max_val = float('inf') * -1
                max_direction = None
                for child in self.succ(state, 1):
                    val, _ = self.search(child, depth - 1, not maximizing_player, alpha, beta)
                    if val > max_val:
                        max_val = val
                        max_direction = child.last_move
                    if max_val > alpha:
                        alpha = max_val
                    if max_val >= beta:
                        return float('inf'), child.last_move
                return max_val, max_direction
            else:
                min_val = float('inf')
                for child in self.succ(state, 2):
                    val, _ = self.search(child, depth - 1, not maximizing_player, alpha, beta)
                    if val < min_val:
                        min_val = val
                    if min_val < beta:
                        beta = min_val
                    if min_val <= alpha:
                        return float('inf') * -1, None
                return min_val, None
