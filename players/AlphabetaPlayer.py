"""
MiniMax Player with AlphaBeta pruning
"""
import time
from players.AbstractPlayer import AbstractPlayer
from SearchAlgos import AlphaBeta
from utils import State


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        super().__init__(game_time, penalty_score)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        self.alpha_beta = AlphaBeta(self.utility, self.succ, self.make_move, self.goal)
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
        return self.make_move_aux(time_limit, players_score)

    def make_move_aux(self, time_limit, players_score, max_depth=float('inf'), set_timer: bool = True, eps=0):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        iter_time = 0
        depth = 1
        val, direction = None, None
        global_start = time.time()
        iter_start = None
        if set_timer:
            self.alpha_beta.setup_timer(time_limit)
        while max_depth >= depth:
            iter_start = time.time()
            if not iter_time or iter_time * (1 + eps) < time_limit - (iter_start - global_start):
                self.alpha_beta.set_end_reason(True)
                try:
                    val, direction = self.alpha_beta.search(self.state, depth, True)
                except TimeoutError:
                    print('TimeoutError catch')
                    break
                if self.alpha_beta.end_reason:
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

    def utility_component1(self, state, turn):
        return state.players_score[0] - state.players_score[1]

    def utility_component2(self, state: State, turn):
        moves = len(state.get_legal_moves(turn))
        if moves == 0:
            return -1
        elif moves == 1:
            return 3
        elif moves == 2:
            return 2
        elif moves == 3:
            return 1
        elif moves == 4:
            return 0

    def utility_component3(self, state: State, turn):
        player_loc = state.players_pos[0] if turn == 1 else state.players_pos[0]
        if not state.fruits_on_board_dict:
            return 0

        md = lambda loc1, loc2: abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])

        def md_wrapper(fruit):
            fruit_loc, fruit_value = fruit
            dist = md(player_loc, fruit_loc)
            if dist < (min(state.size) * 2 - state.total_steps) // 2:
                return 0
            return fruit_value / md(player_loc, fruit_loc)

        fruit_dist = map(md_wrapper, state.fruits_on_board_dict.items())

        return max(fruit_dist)

    def utility_component4(self, state, turn):
        return state.penalty_flag[1] * self.penalty_score - state.penalty_flag[0] * self.penalty_score

    def utility(self, state: State, turn):
        simple_w = 10 if state.fruits_on_board_dict else self.penalty_score // 4
        comp1 = self.utility_component1(state, turn)
        simple = self.utility_component2(state, turn)
        comp3 = self.utility_component3(state, turn)
        comp4 = self.utility_component4(state, turn)
        w1, w3, w4 = 1, 2, 1
        return comp1 * w1 + simple * simple_w + comp3 * w3 + comp4 * w4
