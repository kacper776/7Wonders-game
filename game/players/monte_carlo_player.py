from copy import copy
from random import choice
from math import sqrt, log

from game import *
from heuristics import fill_unknown_information
from players.base_player import AbstractPlayer

INF = 1000000000.0


class MonteCarloPlayer(AbstractPlayer):
    def random_game(self, first_move: Move) -> bool:
        def rotate_hands(game: SevenWonders) -> None:
            dir = [-1, 1, -1][game.age - 1]
            saved_hand = [copy(game.hand[player])
                          for player in range(self.n_players)]
            for player in range(self.n_players):
                game.hand[player] = saved_hand[(player - dir + self.n_players)\
                                                % self.n_players]
        
        def semi_random_move(moves: "list[Move]") -> tuple:
            non_sell_moves = [move for move in moves if move.type != 'sell']
            if non_sell_moves:
                return choice(non_sell_moves)
            return choice(moves)

        game = self.game.copy()
        curr_age = game.age
        first_move_done = False

        if game.free_card_choice == self.nr:
            free_card_move = first_move
            game.do_move(self.nr, free_card_move)
            game.resolve_actions()
            first_move_done = True

        fill_unknown_information(game, self.nr, self.hands_seen,
                                 self.discard_seen)
        
        for age in range(curr_age, 4):
            if age != curr_age:
                game.start_age(age)
            active_players = [player for player in range(self.n_players)
                              if game.hand[player]]   
            while active_players:
                for player in active_players:
                    if not game.moves(player): ###########
                        print(game.hand[player])
                        print(game.free_card_choice)
                    move = semi_random_move(game.moves(player))
                    if not first_move_done and player == self.nr:
                        move = first_move
                        first_move_done = True
                    game.do_move(player, move)
                game.resolve_actions()
                if game.free_card_choice:
                    free_card_move = choice(game.moves(game.free_card_choice))
                    game.do_move(game.free_card_choice, free_card_move)
                    game.resolve_actions()
                if len(game.hand[self.nr]) > 1:
                    rotate_hands(game)
                active_players = [player for player in range(self.n_players)
                                  if game.hand[player]]
            game.end_age(age)

        return self.nr in game.end_game()

    def move_score(self, move: Move, age: int) -> float:
        type_card = (move.type, move.card)
        if self.simulations[type_card] == 0:
            return INF
        exploration_bonus = sqrt(2.0) * sqrt(log(float(self.all_simulations[age])))\
                            / self.simulations[type_card]\
                            if self.all_simulations[age] > 0\
                            else 0
        return self.wins[type_card] / self.simulations[type_card] + exploration_bonus
               

    def do_simulation(self, moves: "list[Move]") -> None:
        age = self.game.age
        first_move = max(moves, key=lambda move: self.move_score(move, age))
        self.all_simulations[age] += 1
        self.simulations[(first_move.type, first_move.card)] += 1
        self.wins[(first_move.type, first_move.card)] += self.random_game(first_move)

    def prepare(self) -> None:
        self.n_simulations = 200
        self.all_simulations = [0, 0, 0, 0]
        self.simulations = {(type, card): 0
                            for type in ('play', 'sell', 'build_wonder')
                            for card in CARDS}
        self.wins = {(type, card): 0
                     for type in ('play', 'sell', 'build_wonder')
                     for card in CARDS}

    def choose_move(self, moves: "list[Move]") -> Move:
        non_sell_moves = [move for move in moves if move.type != 'sell']
        if non_sell_moves:
            moves = non_sell_moves
        for _ in range(self.n_simulations):
            self.do_simulation(moves)
        best_type_and_card = max(moves, key=lambda move: self.wins[(move.type, move.card)]\
                                 / self.simulations[(move.type, move.card)])
        best_moves = [move
                      for move in moves
                      if (move.type, move.card) == (best_type_and_card.type,
                                                    best_type_and_card.card)]
        return min(best_moves, key=lambda move: sum(move.pay_option))