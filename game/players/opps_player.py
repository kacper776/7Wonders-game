from copy import copy
from itertools import product
import cProfile

from game import SevenWonders
from base import *
from players.base_player import AbstractPlayer
from heuristics import move_score, state_score,\
                       fill_unknown_information

N1 = 2
L1 = 3
L2 = 1

INF = 10000.0


# Opponent-prunning paranoid search
def opps(state: SevenWonders, depth: int, nr: int,
         alpha: float=-INF, beta: float=INF) -> "tuple[float][Move]":
    def terminal(state: SevenWonders) -> bool:
        return state.age == 3 and all(map(lambda hand: len(hand) == 0,
                                          state.hand))

    def my_turn(state: SevenWonders) -> bool:
        return len(state.hand[nr]) == len(state.hand[state.left(nr)])

    def rotate_hands(game: SevenWonders) -> None:
        dir = [-1, 1, -1][game.age - 1]
        saved_hand = [copy(game.hand[player])
                      for player in range(game.n_players)]
        for player in range(game.n_players):
            game.hand[player] = saved_hand[(player - dir + game.n_players)\
                                           % game.n_players]

    def resolve_state(state: SevenWonders):
        state.resolve_actions()
        if state.free_card_choice:
            player = state.free_card_choice
            move = max(state.moves(player),
                       key=lambda move: move_score(move, state, player))
            state.do_move(player, move)
            state.resolve_actions()
        if len(state.hand[0]) > 1:
            rotate_hands(state)
        else:
            age = state.age
            state.end_age(age)
            if age < 3:
                state.start_age(age + 1)

    if terminal(state):
        return ((INF if nr in state.end_game() else -INF), None)
    if depth == 0:
        return (state_score(state, nr), None)
    if my_turn(state):
        value = -INF
        best_move = None
        moves = state.moves(nr)
        non_sell_moves = [move for move in moves if move.type != 'sell']
        if non_sell_moves:
            moves = non_sell_moves
        for move in moves:
            new_state = state.copy()
            new_state.do_move(nr, move)
            child_value, _ = opps(new_state, depth - 1, nr, alpha, beta)
            if child_value > value or not best_move:
                best_move = move
            value = max(value, child_value)
            if value >= beta:
                break
            alpha = max(alpha, value)
        return value, best_move

    value = INF
    other_players = list([player for player in range(state.n_players)
                          if player != nr])
    moves = [sorted(state.moves(player),
                    key=lambda move: move_score(move, state, player),
                    reverse=True)
             for player in other_players]
    move_indexes = product(*[range(min(len(moves[other_players.index(player)]), L1))
                             for player in other_players])
    move_indexes = list(filter(lambda idxs: sum(map(lambda idx: (idx >= L2), idxs)) <= N1,
                               move_indexes))
    for idxs in move_indexes:
        new_state = state.copy()
        for i, idx in enumerate(idxs):
            new_state.do_move(other_players[i], moves[i][idx])
        resolve_state(new_state)
        child_value, _ = opps(new_state, depth - 1, nr, alpha, beta)
        value = min(value, child_value)
        if value <= alpha:
            break
        beta = min(beta, value)
    return (value, None)


class OppsPlayer(AbstractPlayer):
    def prepare(self) -> None:
        self.DEPTH = 3
        self.REPEATS = 5

    def choose_move(self, moves: "list[Move]") -> Move:
        if self.game.free_card_choice == self.nr:
            moves = self.game.moves(self.nr)
            return max(moves,
                       key=lambda move: move_score(move, self.game, self.nr))
        move_wins = {move: 0 for move in moves}
        for _ in range(self.REPEATS):
            game = self.game.copy()
            assert(not self.game.free_card_choice)
            fill_unknown_information(game, self.nr,
                                     self.hands_seen, self.discard_seen)
            _, best_move = opps(game, self.DEPTH, self.nr)
            move_wins[best_move] += 1
        # print(sorted(moves,
        #              key=lambda move: move_score(move, self.game, self.nr),
        #              reverse=True))
        # print({move: wins for move, wins in move_wins.items() if wins > 0})
        return max(moves,
                   key=lambda move: (move_wins[move],
                                     move_score(move, self.game, self.nr)))
