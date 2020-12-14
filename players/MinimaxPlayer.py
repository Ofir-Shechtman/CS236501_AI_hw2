"""
MiniMax Player
"""
from players.AbstractPlayer import AbstractPlayer
import numpy as np
from SearchAlgos import MiniMax
from utils import tup_add, get_directions


class State:
    def __init__(self, size, blocks, positions, fruits_on_board_dict, players_score, last_move, total_steps):
        self.size = size
        self.blocks = blocks
        self.players_pos = positions
        self.fruits_on_board_dict = fruits_on_board_dict
        self.players_score = players_score
        self.last_move = last_move
        self.total_steps = total_steps

    @classmethod
    def from_board(cls, board):
        size = board.shape
        blocks = list(map(tuple, np.argwhere(board == -1)))
        my_pos = tuple(np.argwhere(board == 1)[0])
        rival_pos = tuple(np.argwhere(board == 2)[0])
        positions = my_pos,rival_pos
        fruits_on_board_dict = dict()
        for fruit_pos in map(tuple, np.argwhere(board > 2)):
            fruits_on_board_dict[fruit_pos] = board[fruit_pos]
        players_score = (0, 0)
        return cls(size, blocks, positions, fruits_on_board_dict, players_score, None, 0)

    def succ_state(self, turn, new_d):
        if turn == 1:
            new_my_pos = tup_add(self.players_pos[0],new_d)
            new_rival_pos = self.players_pos[1]
        else:
            new_my_pos = self.players_pos[0]
            new_rival_pos = tup_add(self.players_pos[1],new_d)
        new_players_pos = new_my_pos, new_rival_pos
        new_pos_on_board = tup_add(self.players_pos[turn-1], new_d)
        new_blocks = self.blocks.copy()
        if self.total_steps < min(self.size)*2:
            new_fruits_dict = self.fruits_on_board_dict.copy()
        else:
            new_fruits_dict = dict() #all fruits disappeared
        value = 0
        if new_fruits_dict.get(new_pos_on_board):
            value = new_fruits_dict.pop(new_pos_on_board)
        if turn == 1:
            new_players_score = self.players_score[0]+value, self.players_score[1]
        else:
            new_players_score = self.players_score[0], self.players_score[1]+value
        new_blocks.append(self.players_pos[turn-1])
        return State(self.size,
                    new_blocks,
                    new_players_pos,
                    new_fruits_dict,
                    new_players_score,
                    new_d, self.total_steps+1)

    def get_legal_moves(self, turn):
        legal_moves = list()
        for d in get_directions():
            new_pos = tup_add(self.players_pos[turn-1], d)

            # check legal move
            if 0 <= new_pos[0] < self.size[0] and 0 <= new_pos[1] < self.size[1] \
                    and new_pos not in self.blocks and new_pos not in self.players_pos:
                legal_moves.append(d)
        return legal_moves

    def can_move(self, turn):
        return True if self.get_legal_moves(turn) else False

class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time,
                                penalty_score)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        # TODO: initialize more fields, if needed, and the Minimax algorithm from SearchAlgos.py
        self.minmax = MiniMax(self.utility, self.succ, self.make_move, self.goal)
        self.state = None

    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, a 2D matrix of the board.
        No output is expected.
        """
        self.state = State.from_board(board)

    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        #val, direction = self.minmax.search(self.state, float('inf'), True)
        val, direction = self.minmax.search(self.state, 10, True)
        print(val, self.state.players_score)
        self.state = self.state.succ_state(1, direction)
        return direction

    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        direction = pos[0]-self.state.players_pos[1][0], pos[1]-self.state.players_pos[1][1]
        self.state = self.state.succ_state(2, direction)


    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        self.state.fruits_on_board_dict = fruits_on_board_dict
        pass

    ########## helper functions in class ##########


    ########## helper functions for MiniMax algorithm ##########
    # TODO: add here the utility, succ, and perform_move functions used in MiniMax algorithm

    def utility(self, state):
        diff = state.players_score[0] - state.players_score[1]
        if not state.can_move(1):
            diff -= self.penalty_score
        if not state.can_move(2):
            diff += self.penalty_score
        if diff > 0:
            return 1
        elif diff < 0:
            return -1
        else:
            return 0

    @staticmethod
    def succ(state, turn):
        return [state.succ_state(turn, d) for d in state.get_legal_moves(turn)]

    @staticmethod
    def goal(state, turn):
        if not state.can_move(turn):
            return True
        return False
