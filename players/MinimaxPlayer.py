"""
MiniMax Player
"""
from players.AbstractPlayer import AbstractPlayer
import numpy as np
from SearchAlgos import MiniMax
from utils import tup_add, get_directions


class State:
    def __init__(self, size, blocks, my_pos, rival_pos, fruits_on_board_dict, players_score, turn, last_move):
        self.size = size
        self.blocks = blocks
        self.my_pos = my_pos
        self.rival_pos = rival_pos
        self.fruits_on_board_dict = fruits_on_board_dict
        self.players_score = players_score
        self.turn = turn
        self.last_move = last_move

    @classmethod
    def from_board(cls, board, player_turn):
        size = board.shape
        blocks = np.argwhere(board == -1)
        my_pos = np.where(board == 1)
        rival_pos = np.where(board == 2)
        fruits_on_board_dict = dict()
        for fruit_pos in np.argwhere(board > 2):
            fruits_on_board_dict[fruit_pos] = board[fruit_pos]
        players_score = (0, 0)
        return cls(size, blocks, my_pos, rival_pos, fruits_on_board_dict, players_score, player_turn, None)

    def succ_state(self, new_d):
        new_pos = tup_add(self.my_pos, new_d)
        new_fruits_dict = self.fruits_on_board_dict.copy()
        value = 0
        if new_fruits_dict.get(new_pos):
            value = new_fruits_dict.pop(new_pos)
        if self.turn == 1:
            players_score = tup_add(self.players_score, (value, 0))
            return State(self.size,
                         self.blocks.copy().append(self.my_pos),
                         new_pos,
                         self.rival_pos,
                         new_fruits_dict,
                         players_score,
                         2, new_d)
        elif self.turn == 2:
            players_score = tup_add(self.players_score, (0, value))
            return State(self.size,
                         self.blocks.copy().append(self.rival_pos),
                         self.my_pos,
                         new_pos,
                         new_fruits_dict,
                         players_score,
                         1, new_d)


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time,
                                penalty_score)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        # TODO: initialize more fields, if needed, and the Minimax algorithm from SearchAlgos.py
        self.minmax = MiniMax(self.utility, self.succ, self.make_move, self.goal)

    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, a 2D matrix of the board.
        No output is expected.
        """
        self.state = State.from_board(board, player_turn=1)

    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        _, direction = self.minmax.search(self.state, None, True)
        self.state.blocks.append(self.state.my_pos)
        self.state.my_pos = tup_add(self.state.my_pos, direction)
        return direction

    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        self.state.blocks.append(self.state.rival_pos)
        self.state.rival_pos = pos

    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        self.state.fruits_on_board_dict = fruits_on_board_dict

    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed

    ########## helper functions for MiniMax algorithm ##########
    # TODO: add here the utility, succ, and perform_move functions used in MiniMax algorithm

    def utility(self, state):
        diff = state.players_score[0] - state.players_score[1]
        if state.turn == 1:
            diff -= self.penalty_score
        elif state.turn == 2:
            diff += self.penalty_score
        if diff > 0:
            return 1
        elif diff < 0:
            return -1
        else:
            return 0

    @staticmethod
    def get_legal_moves(state):
        legal_moves = list()
        for d in get_directions():
            new_pos = tup_add(state.my_pos, d)

            # check legal move
            if 0 <= new_pos[0] < len(state.size[0]) and 0 <= new_pos[1] < len(state.size[1]) \
                    and (new_pos not in state.blocks + [state.my_pos, state.rival_pos]):
                legal_moves.append(d)
        return legal_moves

    @classmethod
    def succ(cls, state):
        return [state.succ_state(d) for d in cls.get_legal_moves(state)]

    @classmethod
    def goal(cls, state):
        return True if cls.get_legal_moves(state) else False
