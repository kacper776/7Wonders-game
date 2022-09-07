from math import sqrt, log

from game import *
from heuristics import move_score
from random_games import random_game
from players.base_player import AbstractPlayer

INF = 1000000000.0


class MonteCarloPlayer(AbstractPlayer):
    def move_score(self, move: Move, age: int) -> float:
        type_card = (move.type, move.card)
        if self.simulations[type_card] == 0:
            return INF
        exploration_bonus = sqrt(2.0) * sqrt(log(float(self.all_simulations[age])))\
                            / self.simulations[type_card]\
                            if self.all_simulations[age] > 0\
                            else 0
        return self.wins[type_card] / self.simulations[type_card] + exploration_bonus 

    def do_simulation(self, first_move: Move) -> None:
        age = self.game.age
        self.all_simulations[age] += 1
        win, moves_done = random_game(self.game,
                                      first_move, self.nr,
                                      self.hands_seen,
                                      self.discard_seen)
        for move in moves_done:
            self.wins[(move.type, move.card)] += win
            self.simulations[(move.type, move.card)] += 1

    def prepare(self) -> None:
        self.n_simulations = 250
        self.all_simulations = [0, 0, 0, 0]
        self.simulations = {(type, card): 0
                            for type in ('play', 'sell', 'build_wonder')
                            for card in CARDS}
        self.wins = {(type, card): 0
                     for type in ('play', 'sell', 'build_wonder')
                     for card in CARDS}

    def choose_move(self, moves: "list[Move]") -> Move:
        if self.game.free_card_player == self.nr:
            return max(moves, key=lambda move: move_score(move,
                                                          self.game,
                                                          self.nr))
        # non_sell_moves = [move for move in moves if move.type != 'sell']
        # if non_sell_moves:
        #     moves = non_sell_moves
        for _ in range(self.n_simulations):
            self.do_simulation(max(moves, key=lambda move: self.move_score(move,
                                                                           self.game.age)))
        best_type_and_card = max(moves, key=lambda move: self.wins[(move.type, move.card)]\
                                 / self.simulations[(move.type, move.card)])
        best_moves = [move
                      for move in moves
                      if (move.type, move.card) == (best_type_and_card.type,
                                                    best_type_and_card.card)]
        return min(best_moves, key=lambda move: sum(move.pay_option))