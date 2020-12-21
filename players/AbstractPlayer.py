"""Abstract class of player. 
Your players classes must inherit from this.
"""
import utils
import time
import numpy as np
from SearchAlgos import SearchAlgos


class State:
    def __init__(self, size, blocks, positions, fruits_on_board_dict, players_score, last_move, total_steps,
                 penalty_flag):
        self.size = size
        self.blocks = blocks
        self.players_pos = positions
        self.fruits_on_board_dict = fruits_on_board_dict
        self.players_score = players_score
        self.last_move = last_move
        self.total_steps = total_steps
        self.penalty_flag = penalty_flag

    @classmethod
    def from_board(cls, board):
        size = board.shape
        blocks = list(map(tuple, np.argwhere(board == -1)))
        my_pos = tuple(np.argwhere(board == 1)[0])
        rival_pos = tuple(np.argwhere(board == 2)[0])
        positions = my_pos, rival_pos
        fruits_on_board_dict = dict()
        for fruit_pos in map(tuple, np.argwhere(board > 2)):
            fruits_on_board_dict[fruit_pos] = board[fruit_pos]
        players_score = (0, 0)
        penalty_flag = [False, False]
        return cls(size, blocks, positions, fruits_on_board_dict, players_score, None, 0, penalty_flag)

    def succ_state(self, turn, new_d):
        if turn == 1:
            new_my_pos = utils.tup_add(self.players_pos[0], new_d)
            new_rival_pos = self.players_pos[1]
        else:
            new_my_pos = self.players_pos[0]
            new_rival_pos = utils.tup_add(self.players_pos[1], new_d)
        new_players_pos = new_my_pos, new_rival_pos
        new_pos_on_board = utils.tup_add(self.players_pos[turn - 1], new_d)
        new_blocks = self.blocks.copy()
        if self.total_steps < min(self.size) * 2:
            new_fruits_dict = self.fruits_on_board_dict.copy()
        else:
            new_fruits_dict = dict()  # all fruits disappeared
        value = 0
        if new_fruits_dict.get(new_pos_on_board):
            value = new_fruits_dict.pop(new_pos_on_board)
        if turn == 1:
            new_players_score = self.players_score[0] + value, self.players_score[1]
        else:
            new_players_score = self.players_score[0], self.players_score[1] + value
        new_blocks.append(self.players_pos[turn - 1])
        new_state = State(self.size,
                          new_blocks,
                          new_players_pos,
                          new_fruits_dict,
                          new_players_score,
                          new_d,
                          self.total_steps + 1,
                          self.penalty_flag.copy())
        other_turn = 3 - turn
        if new_state.total_steps % 2:
            if not new_state.can_move(turn):
                new_state.penalty_flag[turn - 1] = True
        else:
            if not new_state.can_move(turn):
                new_state.penalty_flag[turn - 1] = True
            if not new_state.can_move(other_turn):
                new_state.penalty_flag[other_turn - 1] = True


        '''turn = 3-turn
        if not new_state.can_move(turn):
            if turn==1:
                new_state.players_score = new_state.players_score[0]-new_state.penalty_score, new_state.players_score[1]
            elif turn==2:
                new_state.players_score = new_state.players_score[0], new_state.players_score[1]-new_state.penalty_score'''
        return new_state

    def get_legal_moves(self, turn):
        legal_moves = list()
        for d in utils.get_directions():
            new_pos = utils.tup_add(self.players_pos[turn - 1], d)

            # check legal move
            if 0 <= new_pos[0] < self.size[0] and 0 <= new_pos[1] < self.size[1] \
                    and new_pos not in self.blocks and new_pos not in self.players_pos:
                legal_moves.append(d)
        return legal_moves

    def can_move(self, turn):
        return True if self.get_legal_moves(turn) else False


class AbstractPlayer:
    """Your player must inherit from this class.
    Your player class name must be 'Player', as in the given examples (SimplePlayer, LivePlayer).
    Use like this:
    from players.AbstractPlayer import AbstractPlayer
    class Player(AbstractPlayer):
    """

    def __init__(self, game_time, penalty_score):
        """
        Player initialization.
        """
        self.game_time = game_time
        self.penalty_score = penalty_score
        self.directions = utils.get_directions()  # [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.search_algorithm = SearchAlgos(self.utility,self.succ, self.make_move, self.goal)
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
        iter_time = 0
        eps = 0.5
        depth = 1
        val, direction = None, None
        global_start = time.time()
        while True:
            iter_start = time.time()
            if not iter_time or iter_time * (1 + eps) < time_limit - (iter_start - global_start):
                self.search_algorithm.set_end_reason(True)
                val, direction = self.search_algorithm.search(self.state, depth, True)
                if self.search_algorithm.end_reason:
                    print('end_reason')
                    break
                iter_time = time.time() - iter_start
                depth += 1
            else:
                break
        print(depth, iter_start - global_start, iter_time)

        print(val, self.state.players_score)
        self.state = self.state.succ_state(1, direction)
        return direction

    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        direction = pos[0] - self.state.players_pos[1][0], pos[1] - self.state.players_pos[1][1]
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

    @staticmethod
    def succ(state, turn):
        return [state.succ_state(turn, d) for d in state.get_legal_moves(turn)]

    @staticmethod
    def goal(state, turn):
        if not state.can_move(turn):
            return True
        return False

    def utility(self, state):
        score = list(state.players_score)
        for i in range(2):
            if state.penalty_flag[i]:
                score[i] -= self.penalty_score
        return score[0]-score[1]