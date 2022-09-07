from functools import partial

from base import *

READY = 1
USED = 0


def no_effect(game, player):
    pass


def combined_effects(game, player: int, effects: tuple):
    for effect in effects:
        effect(game, player)

def combine_effects(*effects):
    return partial(combined_effects, effects=effects)


def add_resource(game, player: int, resource: Resources):
        game.resources[player] = list(map(lambda res_option: res_option + resource, game.resources[player]))

def resource_effect(resource: Resources):
    return partial(add_resource, resource=resource)


def add_points(game, player: int, points: int):
        game.points[player] += points

def points_effect(points: int):
    return partial(add_points, points=points)


def add_coins(game, player: int, coins: int):
        game.coins[player] += coins

def coins_effect(coins: int):
    return partial(add_coins, coins=coins)


def add_exclusive_resources(game, player: int, resource1: Resources, resource2: Resources):
        res = []
        for resource_option in game.resources[player]:
            res.append(resource_option + resource1)
            res.append(resource_option + resource2)
        game.resources[player] = res

def exclusive_resources_effect(resource1: Resources, resource2: Resources):
    return partial(add_exclusive_resources, resource1=resource1, resource2=resource2)


def add_points_for_neighbours_cards(game, player: int, colour: str):
        game.points[player] += len(set(filter(lambda card: card.colour == colour,
                                              game.board[game.left(player)])))
        game.points[player] += len(set(filter(lambda card: card.colour == colour,
                                              game.board[game.right(player)])))

def neighbours_cards_points_effect(colour: str):
    return partial(add_points_for_neighbours_cards, colour=colour)


def strategists_guild_effect(game, player):
    game.points[player] += game.tokens[game.left(player)].count(-1)
    game.points[player] += game.tokens[game.right(player)].count(-1)


def scientists_guild_effect(game, player):
    best_points = 0
    best_symbols = game.scientific_symbols[player]
    for symbol in (ScientificSymbols(slate=1),
                   ScientificSymbols(cog=1),
                   ScientificSymbols(compass=1)):
        new_symbols = game.scientific_symbols[player] + symbol
        if new_symbols.points() > best_points:
            best_points = new_symbols.points()
            best_symbols = new_symbols
    game.scientific_symbols[player] = best_symbols


def builders_guild_effect(game, player: int):
    game.points[player] += game.wonder_stages[player]
    game.points[player] += game.wonder_stages[game.left(player)]
    game.points[player] += game.wonder_stages[game.right(player)]


def set_raw_cost_to_1(game, player: int, dir: int):
        game.raw_costs[player][dir] = 1

def trading_post_effect(dir: int):
    return partial(set_raw_cost_to_1, dir=dir)


def marketplace_effect(game, player):
    game.refined_costs[player] = (1, 1)


def add_untradable_resources(game, player: int, resources: "tuple[Resources]"):
        res = []
        for resource in game.untradable_resources[player]:
            for new_resource in resources:
                res.append(resource + new_resource)
        game.untradable_resources[player] = res

def untradable_resources_effect(*resources):
    return partial(add_untradable_resources, resources=resources)


def add_points_for_your_cards(game, player: int, colour: str, points: int):
        game.points[player] += points * len(set(filter(lambda card: card.colour == colour,
                                                       game.board[player])))

def your_cards_points_effect(colour: str, points: int):
    return partial(add_points_for_your_cards, colour=colour, points=points)


def add_coins_for_your_cards(game, player: int, colour: str, coins: int):
        game.coins[player] += coins * len(set(filter(lambda card: card.colour == colour,
                                                     game.board[player])))

def your_cards_coins_effect(colour: str, coins: int):
    return partial(add_coins_for_your_cards, colour=colour, coins=coins)


def vineyard_effect(game, player: int):
    game.coins[player] += len(set(filter(lambda card: card.colour == 'brown',
                                         game.board[player])))
    game.coins[player] += len(set(filter(lambda card: card.colour == 'brown',
                                         game.board[game.left(player)])))
    game.coins[player] += len(set(filter(lambda card: card.colour == 'brown',
                                         game.board[game.right(player)])))


def bazar_effect(game, player: int):
    game.coins[player] += 2 * len(set(filter(lambda card: card.colour == 'gray',
                                             game.board[player])))
    game.coins[player] += 2 * len(set(filter(lambda card: card.colour == 'gray',
                                             game.board[game.left(player)])))
    game.coins[player] += 2 * len(set(filter(lambda card: card.colour == 'gray',
                                             game.board[game.right(player)])))


def add_shields(game, player: int, shields: int):
        game.shields[player] += shields

def shields_effect(shields: int):
    return partial(add_shields, shields=shields)


def add_symbol(game, player: int, symbol: ScientificSymbols):
        game.scientific_symbols[player] += symbol

def scientific_symbol_effect(symbol: ScientificSymbols):
    return partial(add_symbol, symbol=symbol)


def arena_immediate_effect(game, player: int):
    game.coins[player] += 3 * game.wonder_stages[player]


def arena_end_game_effect(game, player: int):
    game.points[player] += game.wonder_stages[player]


def free_card_per_age_effect(game, player: int):
    game.special_powers[player].append(('free_card_per_age', READY))


def free_card_from_discard_effect(game, player: int):
    if [card for card in game.discard_pile if card not in game.board[player]]:
        game.special_powers[player].append(('free_card_from_discard', READY))


def play_last_card_effect(game, player: int):
    game.special_powers[player].append(('play_last_card', READY))


def copy_guild_effect(game, player: int):
    curr_points = game.points[player]
    best_points = game.points[player]
    neighbours_guilds = set(filter(lambda card: card.colour == 'guild',
                                   game.board[game.left(player)].union(\
                                   game.board[game.right(player)])))
    for guild in neighbours_guilds:
        guild.end_game_effect(game, player)
        best_points = max(best_points, game.points[player])
        game.points[player] = curr_points
    
    game.points[player] = best_points
