import operator
import numpy as np
import os

#TODO: edit the alpha and beta initialization values for AlphaBeta algorithm.
# instead of 'None', write the real initialization value, learned in class.
# hint: you can use np.inf
ALPHA_VALUE_INIT = float('inf') * -1
BETA_VALUE_INIT = float('inf')

def get_directions():
    """Returns all the possible directions of a player in the game as a list of tuples.
    """
    return [(1, 0), (0, 1), (-1, 0), (0, -1)]


def tup_add(t1, t2):
    """
    returns the sum of two tuples as tuple.
    """
    return tuple(map(operator.add, t1, t2))


def get_board_from_csv(board_file_name):
    """Returns the board data that is saved as a csv file in 'boards' folder.
    The board data is a list that contains: 
        [0] size of board
        [1] blocked poses on board
        [2] starts poses of the players
    """
    board_path = os.path.join('boards', board_file_name)
    board = np.loadtxt(open(board_path, "rb"), delimiter=" ")
    
    # mirror board
    board = np.flipud(board)
    i, j = len(board), len(board[0])
    blocks = np.where(board == -1)
    blocks = [(blocks[0][i], blocks[1][i]) for i in range(len(blocks[0]))]
    start_player_1 = np.where(board == 1)
    start_player_2 = np.where(board == 2)
    
    if len(start_player_1[0]) != 1 or len(start_player_2[0]) != 1:
        raise Exception('The given board is not legal - too many start locations.')
    
    start_player_1 = (start_player_1[0][0], start_player_1[1][0])
    start_player_2 = (start_player_2[0][0], start_player_2[1][0])

    return [(i, j), blocks, [start_player_1, start_player_2]]



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
            new_my_pos = tup_add(self.players_pos[0], new_d)
            new_rival_pos = self.players_pos[1]
        else:
            new_my_pos = self.players_pos[0]
            new_rival_pos = tup_add(self.players_pos[1], new_d)
        new_players_pos = new_my_pos, new_rival_pos
        new_pos_on_board = tup_add(self.players_pos[turn - 1], new_d)
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
        for d in get_directions():
            new_pos = tup_add(self.players_pos[turn - 1], d)

            # check legal move
            if 0 <= new_pos[0] < self.size[0] and 0 <= new_pos[1] < self.size[1] \
                    and new_pos not in self.blocks and new_pos not in self.players_pos:
                legal_moves.append(d)
        return legal_moves

    def can_move(self, turn):
        return True if self.get_legal_moves(turn) else False
