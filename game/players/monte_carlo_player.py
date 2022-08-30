from copy import deepcopy, copy
from random import choice
from math import sqrt, log

from game import *
from players.base_player import AbstractPlayer

INF = 1000000000.0


class MonteCarloPlayer(AbstractPlayer):
    def random_game(self, first_move: tuple) -> bool:
        def rotate_hands(game: SevenWonders, age: int) -> None:
            dir = [1, -1, 1][age - 1]
            saved_hand = [copy(game.hand[player]) for player in range(self.n_players)]
            for player in range(self.n_players):
                game.hand[player] = saved_hand[(player - dir + self.n_players) % self.n_players]

        def fill_other_players_hands(game: SevenWonders, age: int) -> None:
            curr_hand_size = len(game.hand[self.nr])
            age_cards = [card for card in CARDS
                         for players in range(2, self.n_players + 1)
                         if card.age == age and players in card.copies]
            for player in range(self.n_players):
                for card in game.board[player]:
                    if card in age_cards:
                        age_cards.remove(card) 
            for card in game.hand[self.nr]:
                age_cards.remove(card)

            for player in range(self.n_players):
                if player == self.nr:
                    continue
                game.hand[player] = sample(age_cards, curr_hand_size)
                for card in game.hand[player]:
                    age_cards.remove(card)
        
        def semi_random_move(moves: "tuple[tuple]") -> tuple:
            non_sell_moves = [move for move in moves if move[0] != 'sell']
            if non_sell_moves:
                return choice(non_sell_moves)
            move = choice(moves)
            return move

        game = deepcopy(self.game)
        game.verbose = False
        curr_age = game.age
        first_move_done = False
        fill_other_players_hands(game, curr_age)

        if game.free_card_choice == self.nr:
            free_card_move = first_move
            game.do_move(self.nr, free_card_move)
            game.resolve_actions()
            first_move_done = True
        
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
                    rotate_hands(game, age)
                active_players = [player for player in range(self.n_players)
                                  if game.hand[player]]
            game.end_age(age)

        return self.nr in game.end_game()

    def move_score(self, move: tuple, age: int) -> float:
        type, (card, option) = move
        type_card = (type, card)
        if self.simulations[type_card] == 0:
            return INF
        exploration_bonus = sqrt(2.0) * sqrt(log(float(self.all_simulations[age])))\
                            / self.simulations[type_card]\
                            if self.all_simulations[age] > 0\
                            else 0
        return self.wins[type_card] / self.simulations[type_card] + exploration_bonus
               

    def do_simulation(self, moves: "tuple[tuple]") -> None:
        age = self.game.age
        first_move = max(moves, key=lambda move: self.move_score(move, age))
        type, (card, option) = first_move
        self.all_simulations[age] += 1
        self.simulations[(type, card)] += 1
        self.wins[(type, card)] += self.random_game(first_move)

    def prepare(self) -> None:
        self.n_simulations = 200
        self.all_simulations = [0, 0, 0, 0]
        self.simulations = {(type, card): 0
                            for type in ('play', 'sell', 'build_wonder')
                            for card in CARDS}
        self.wins = {(type, card): 0
                     for type in ('play', 'sell', 'build_wonder')
                     for card in CARDS}

    def choose_move(self, moves: "tuple[tuple]") -> tuple:
        for _ in range(self.n_simulations):
            self.do_simulation(moves)
        best_type_and_card = max(moves, key=lambda move:
                                            self.simulations[(move[0], move[1][0])])
        best_moves = [(type, (card, option))
                      for type, (card, option) in moves
                      if (type, card) == (best_type_and_card[0], best_type_and_card[1][0])]
        return min(best_moves, key=lambda move: sum(move[1][1]))