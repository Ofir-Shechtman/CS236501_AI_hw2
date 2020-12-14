"""Search Algos: MiniMax, AlphaBeta
"""
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

    def search(self, state, depth, maximizing_player):
        pass


class MiniMax(SearchAlgos):

    def search(self, state, depth, maximizing_player):
        """Start the MiniMax algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        if self.goal(state):
            return self.utility(state), None
        else:









            succ_res = map(self.succ(state), lambda child: self.search(child, depth - 1, not maximizing_player))
            key= lambda res: res[0]
            if maximizing_player:
                return max(succ_res, key=key)
            else:
                return min(succ_res, key=key)



            next_pos = -1
            for child in self.succ(state):
                if maximizing_player == 1:
                    if self.search(child, depth - 1, not maximizing_player)[0] == 1:
                        next_state = child
            return next_state.d

        next = self.utility(state)
        for child in self.succ(state):
            value, direction = self.search((child, depth - 1, not maximizing_player))

        return


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
        # TODO: erase the following line and implement this function.
        raise NotImplementedError
