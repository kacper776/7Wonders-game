from random import choice
from copy import deepcopy

from base import *
from cards import CARDS
from game import SevenWonders
from players.base_player import AbstractPlayer

def resource_score(game: SevenWonders, nr: int, n_players: int) -> int:
    cards_in_play = [card for card in CARDS
                        for players in range(2, n_players + 1)
                        if players in card.copies]
    for player in range(n_players):
        for card in game.board[player]:
            cards_in_play.remove(card)
    can_buy = [card for card in cards_in_play
                    if game.pay_options(nr, card.cost)]
    my_raw = game.resources[nr][0].raw_cnt()
    my_refined = game.resources[nr][0].refined_cnt()
    discounted_raw = game.resources[game.left(nr)][0].raw_cnt()\
                        * (game.raw_costs[nr][0] == 1)\
                     + game.resources[game.right(nr)][0].raw_cnt()\
                        * (game.raw_costs[nr][1] == 1)
    discounted_refined = game.resources[game.left(nr)][0].refined_cnt()\
                        * (game.refined_costs[nr][0] == 1)\
                     + game.resources[game.right(nr)][0].refined_cnt()\
                        * (game.refined_costs[nr][1] == 1)
    return 0.5 * len(can_buy) + 1.5 * my_raw + 2 * my_refined +\
           0.8 * discounted_raw + discounted_refined

def points_score(game: SevenWonders, nr: int) -> int:
    return game.points[nr]

def battle_score(game: SevenWonders, nr: int, age: int) -> int:
    win_score = [1.2, 3.1, 5.0]
    draw_score = [0.2, 0.6, 1.4]
    battle_wins = int(game.shields[nr] > game.shields[game.left(nr)]) +\
                    int(game.shields[nr] > game.shields[game.right(nr)])
    battle_draws = int(game.shields[nr] == game.shields[game.left(nr)]) +\
                    int(game.shields[nr] == game.shields[game.right(nr)])
    return win_score[age-1] * battle_wins + draw_score[age-1] * battle_draws

def coins_score(game: SevenWonders, nr: int) -> int:
    return 0.4 * game.coins[nr]

def science_score(game: SevenWonders, nr: int, age: int) -> int:
    age_science_bonus = [1.5, 0.5, 0.0]
    return age_science_bonus[age-1] * game.scientific_symbols[nr].cnt()

def overall_score(game: SevenWonders, nr: int, age: int, n_players: int) -> int:
    return resource_score(game, nr, n_players) + points_score(game, nr) +\
           battle_score(game, nr, age) + coins_score(game, nr) +\
           science_score(game, nr, age)

def card_score(game: SevenWonders, nr: int, card: Card,
              can_improve: bool=False) -> int:
    n_players = len(game.board)
    age = game.age

    score_before = overall_score(game, nr, age, n_players)

    card.immediate_effect(game, nr)
    card.end_game_effect(game, nr)
    game.board[nr].add(card)

    score_after = overall_score(game, nr, age, n_players)
    return score_after - score_before + int(can_improve)


def wonder_stage_score(game: SevenWonders, nr: int,
                       stage: WonderStage) -> int:
    n_players = len(game.board)
    age = game.age

    score_before = overall_score(game, nr, age, n_players)

    stage.immediate_effect(game, nr)
    stage.end_game_effect(game, nr)

    score_after = overall_score(game, nr, age, n_players)
    return score_after - score_before

class ScorePlayer(AbstractPlayer):
    def prepare(self) -> None:
        self.improving_cards = {
            'traders_guild',
            'philosophers_guild',
            'spies_guild',
            'strategist_guild',
            'shipowners_guild',
            'scientists_guild',
            'magistrates_guild',
            'builders_guild',
            'haven',
            'lighthouse',
            'arena'
        }
        self.olympiaA_second_stage_scores = [6, 4.5, 3]
        self.babylonB_second_stage_scores = [7, 5.5, 2]
        self.card_from_discard_scores = [0, 4, 6, 8]

    def move_score(self, move: tuple):
        type, (card, pay_option) = move
        if type == 'play':
            coins_to_pay = sum(pay_option) + card.cost.coins
            return card_score(deepcopy(self.game), self.nr, card,
                              card.name in self.improving_cards)\
                   - 0.4 * coins_to_pay
        if type == 'build_wonder':
            wonder = self.game.wonders[self.nr]
            stage_nr = self.game.wonder_stages[self.nr]
            age = self.game.age
            stage = wonder.stages[stage_nr]
            coins_to_pay = sum(pay_option)

            if wonder.name == 'olympia(A)' and stage_nr == 1:
                return self.olympiaA_second_stage_scores[age-1]\
                       - 0.4 * coins_to_pay
            if wonder.name == 'babylon(B)' and stage_nr == 1:
                return self.babylonB_second_stage_scores[age-1]\
                       - 0.4 * coins_to_pay
            if wonder.name == 'halikarnassos(A)' and stage_nr == 1:
                last_card_in_age = int(len(self.game.hand[self.nr]) == 2)
                return self.card_from_discard_scores[age-1 + last_card_in_age]\
                       - 0.4 * coins_to_pay
            if wonder.name == 'halikarnassos(B)':
                last_card_in_age = int(len(self.game.hand[self.nr]) == 2)
                return self.card_from_discard_scores[age-1 + last_card_in_age]\
                       + 2 - stage_nr - 0.4 * coins_to_pay

            return wonder_stage_score(deepcopy(self.game), self.nr, stage)\
                   - 0.4 * coins_to_pay

    def choose_move(self, moves: "tuple[tuple]") -> tuple:
        for move in moves:
            if move[0] == 'sell':
                continue
            print(move, end=' ')
            print(self.move_score(move))
        print()
        non_sell_moves = [move for move in moves if move[0] != 'sell']
        sell_moves = [move for move in moves if move[0] == 'sell']
        best_non_sell_move = max(non_sell_moves, key=self.move_score, default=None)
        if not sell_moves:
            return best_non_sell_move
        if not best_non_sell_move or self.move_score(best_non_sell_move) < 1.2:
            return choice(sell_moves)
        return best_non_sell_move
