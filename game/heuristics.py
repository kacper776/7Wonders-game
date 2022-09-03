from random import sample

from base import *
from cards import CARDS
from game import SevenWonders


def resource_score(game: SevenWonders, nr: int) -> float:
    n_players = len(game.board)
    age = game.age
    cards_in_play = [card for card in CARDS
                     for players in range(2, n_players + 1)
                     if players in card.copies]
    for player in range(n_players):
        for card in game.board[player]:
            cards_in_play.remove(card)
    can_buy = [card for card in cards_in_play
                    if game.pay_options(nr, card.cost)]
    can_build = [stage for stage in game.wonders[nr].stages[game.wonder_stages[nr]:]
                 if game.pay_options(nr, stage.cost)]
    my_raw = game.resources[nr][0].raw_cnt()
    my_refined = game.resources[nr][0].refined_cnt()
    discounted_raw = game.resources[game.left(nr)][0].raw_cnt()\
                        * (game.raw_costs[nr][0] == 1)\
                     + game.resources[game.right(nr)][0].raw_cnt()\
                        * int(game.raw_costs[nr][1] == 1)
    discounted_refined = game.resources[game.left(nr)][0].refined_cnt()\
                            * (game.refined_costs[nr][0] == 1)\
                         + game.resources[game.right(nr)][0].refined_cnt()\
                            * int(game.refined_costs[nr][1] == 1)
    return 0.4 * len(can_buy) + len(can_build) + 1.3/age * my_raw + 1.7/age * my_refined +\
           0.8 * discounted_raw + discounted_refined

def points_score(game: SevenWonders, nr: int) -> float:
    return game.points[nr]

def battle_score(game: SevenWonders, nr: int) -> float:
    win_score = [1.7, 3.1, 4.5]
    age = game.age
    battle_wins = int(game.shields[nr] > game.shields[game.left(nr)]) +\
                  int(game.shields[nr] > game.shields[game.right(nr)])
    battle_draws = int(game.shields[nr] == game.shields[game.left(nr)]) +\
                   int(game.shields[nr] == game.shields[game.right(nr)])
    return win_score[age-1] * battle_wins + battle_draws\
           + game.shields[nr] / age

def coins_score(game: SevenWonders, nr: int) -> float:
    return 0.4 * game.coins[nr]

def science_score(game: SevenWonders, nr: int) -> float:
    age = game.age
    age_science_bonus = [1.8, 1.0, 0.0]
    return age_science_bonus[age-1] * game.scientific_symbols[nr].cnt()\
           + game.scientific_symbols[nr].points()

def special_score(game: SevenWonders, nr: int):
    improving_cards = {
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
    olympiaA_second_stage_scores = [5, 3.5, 2]
    babylonB_second_stage_scores = [7, 5.5, 2]
    card_from_discard_scores = [0, 4, 6, 8]
    age = game.age
    score = 0.0
    for power, ready in game.special_powers[nr]:
        if power == 'free_card_from_discard' and ready:
            last_card_in_age = int(len(game.hand[nr]) == 2)
            score += card_from_discard_scores[age-1 + last_card_in_age]
        if power == 'free_card_per_age':
            score += olympiaA_second_stage_scores[age-1]
            if ready:
                score += 1.0
        if power == 'play_last_card':
            score += babylonB_second_stage_scores[age-1]
    score += len([card.name for card in game.board[nr]
                  if card.name in improving_cards])
    return score
    


def overall_score(game: SevenWonders, nr: int) -> float:
    return resource_score(game, nr) + points_score(game, nr) +\
           battle_score(game, nr) + coins_score(game, nr) +\
           science_score(game, nr) + special_score(game, nr)

def card_score(game: SevenWonders, nr: int, card: Card) -> float:
    score_before = overall_score(game, nr)

    card.immediate_effect(game, nr)
    card.end_game_effect(game, nr)
    game.board[nr].add(card)

    score_after = overall_score(game, nr)
    return score_after - score_before


def wonder_stage_score(game: SevenWonders, nr: int,
                       stage: WonderStage) -> float:
    score_before = overall_score(game, nr)

    stage.immediate_effect(game, nr)
    stage.end_game_effect(game, nr)

    score_after = overall_score(game, nr)
    return score_after - score_before


def move_score(move: Move, game: SevenWonders, nr: int) -> float:
    if move.type == 'play':
        coins_to_pay = max(0, sum(move.pay_option)) + move.card.cost.coins
        return card_score(game.copy(), nr, move.card)\
                - 0.4 * coins_to_pay

    if move.type == 'build_wonder':
        wonder = game.wonders[nr]
        stage_nr = game.wonder_stages[nr]
        stage = wonder.stages[stage_nr]
        coins_to_pay = max(0, sum(move.pay_option))
        return wonder_stage_score(game.copy(), nr, stage)\
                - 0.4 * coins_to_pay

    if move.type == 'sell':
        return 1.2


def state_score(game: SevenWonders, nr: int):
    result_score = overall_score(game, nr)
    other_scores = []
    for player in range(game.n_players):
        if player == nr:
            continue
        other_scores.append(overall_score(game, player))
    other_scores = sorted(other_scores, reverse=True)
    mult = 0.2
    for score in other_scores:
        result_score -= score * mult
        mult -= 0.1
    return result_score        


def fill_unknown_information(game: SevenWonders, nr: int,
                             hands_seen: "list[list[Card]]",
                             discard_seen: "list[Card]") -> None:
    def next(player: int, game: SevenWonders):
        if game.age == 2:
            return game.right(player)
        return game.left(player)

    n_players = len(game.board)
    age = game.age
    curr_hand_size = len(game.hand[nr])
    age_cards = [card for card in CARDS
                 for players in range(2, n_players + 1)
                 if card.age == age and players in card.copies]

    for player in range(n_players):
        for card in game.board[player]:
            if card in age_cards:
                age_cards.remove(card)
    for card in discard_seen:
        if card in age_cards:
            age_cards.remove(card)
    
    for card in game.hand[nr]:
        age_cards.remove(card)

    hand_owner = next(nr, game)
    for hand in reversed(hands_seen):
        if hand_owner == nr:
            break
        game.hand[hand_owner] = []
        for card in hand:
            if len(game.hand[hand_owner]) == curr_hand_size:
                break
            if card in age_cards:
                age_cards.remove(card)
                game.hand[hand_owner].append(card)
        hand_owner = next(hand_owner, game)

    for player in range(n_players):
        if player == nr:
            continue
        if not game.hand[player]:
            game.hand[player] = []
        hand_fill = sample(age_cards, curr_hand_size - len(game.hand[player]))
        for card in hand_fill:
            age_cards.remove(card)
            game.hand[player].append(card)

    game.discard_pile = age_cards
