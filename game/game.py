from random import sample
from math import floor
from copy import copy

from base import *
from effects import *
from cards import CARDS


class SevenWonders(object):
    CONFLICT_TOKENS = (-1, 1, 3, 5)
    SPECIAL_OLYPMIA = -1
    SPECIAL_DISCARD = -2
    FREE_OPTION = (0, 0)

    def __init__(self, n_players: int, wonders: "tuple[Wonder]",
                 verbose: bool=False) -> None:
        # general
        self.verbose = verbose
        self.n_players = n_players
        self.discard_pile = []
        self.actions_queue = []
        self.free_card_player = None
        self.age = 0
        self.deck = [[card for card in CARDS
                      for players in range(2, n_players + 1)
                      if card.age == age and players in card.copies
                         and card.colour != 'guild']
                     for age in range(1, 4)]

        # per player
        self.board = [set() for _ in range(n_players)]
        self.hand = [None] * n_players
        self.wonders = wonders
        self.wonder_stages = [0] * n_players
        self.coins = [START_COINS] * n_players
        self.points = [0] * n_players
        self.shields = [0] * n_players
        self.scientific_symbols = [ScientificSymbols() for _ in range(n_players)]
        self.tokens = []
        for _ in range(n_players):
            self.tokens.append([])
        self.resources = [[wonder.starting_resource] for wonder in wonders]
        self.untradable_resources = [[Resources()]] * n_players
        self.raw_costs = [[2, 2] for _ in range(n_players)]
        self.refined_costs = [[2, 2] for _ in range(n_players)]
        self.special_powers = []
        for _ in range(n_players):
            self.special_powers.append([])

    def copy(self):
        result = SevenWonders(self.n_players, self.wonders)
        result.discard_pile = copy(self.discard_pile)
        result.actions_queue = copy(self.actions_queue)
        result.free_card_player = self.free_card_player
        result.age = self.age
        result.deck = []
        for age_deck in self.deck:
            result.deck.append(copy(age_deck))
        result.board = []
        for player_board in self.board:
            result.board.append(copy(player_board))
        result.hand = []
        for player_hand in self.hand:
            result.hand.append(copy(player_hand))
        result.wonder_stages = copy(self.wonder_stages)
        result.coins = copy(self.coins)
        result.points = copy(self.points)
        result.shields = copy(self.shields)
        result.scientific_symbols = []
        for player_symbols in self.scientific_symbols:
            result.scientific_symbols.append(copy(player_symbols))
        result.tokens = []
        for player_tokens in self.tokens:
            result.tokens.append(copy(player_tokens))
        result.resources = []
        for player_resources in self.resources:
            result.resources.append(copy(player_resources))
        result.untradable_resources = []
        for player_untradable_resources in self.untradable_resources:
            result.untradable_resources.append(copy(player_untradable_resources))
        result.raw_costs = []
        for player_raw_costs in self.raw_costs:
            result.raw_costs.append(copy(player_raw_costs))
        result.refined_costs = []
        for player_refined_costs in self.refined_costs:
            result.refined_costs.append(copy(player_refined_costs))
        result.special_powers = []
        for player_powers in self.special_powers:
            result.special_powers.append(copy(player_powers))
        return result

    def left(self, player: int) -> int:
        return (player - 1 + self.n_players) % self.n_players

    def right(self, player: int) -> int:
        return (player + 1) % self.n_players

    def start_age(self, age: int) -> None:
        if self.verbose:
            print(f'starting age {age}')
        self.age = age
        if age == 3:
            guilds = [card for card in CARDS if card.colour == 'guild']
            guilds_in_play = sample(guilds, self.n_players + 2)
            self.deck[2].extend(guilds_in_play)
        age_cards = self.deck[age - 1]
        assert(len(age_cards) == MAX_HAND * self.n_players)
        for player in range(self.n_players):
            self.hand[player] = sample(age_cards, MAX_HAND)
            for card in self.hand[player]:
                age_cards.remove(card)
            for i, (power, ready) in enumerate(self.special_powers[player]):
                if power == 'free_card_per_age':
                    self.special_powers[player][i] = ('free_card_per_age', READY)
                    break

    def end_age(self, age: int, player_names: "list[str]"=None) -> None:
        if self.verbose:
            print(f'ending age {age}')
        for player in range(self.n_players):
            new_tokens = []
            if self.shields[player] > self.shields[self.left(player)]:
                new_tokens.append(self.CONFLICT_TOKENS[age])
            elif self.shields[player] < self.shields[self.left(player)]:
                new_tokens.append(self.CONFLICT_TOKENS[0])
            if self.shields[player] > self.shields[self.right(player)]:
                new_tokens.append(self.CONFLICT_TOKENS[age])
            elif self.shields[player] < self.shields[self.right(player)]:
                new_tokens.append(self.CONFLICT_TOKENS[0])
            self.tokens[player].extend(new_tokens)
            if self.verbose:
                print(f'{player_names[player]} got {sorted(new_tokens)} tokens')

    def end_game(self) -> "list[int]":
        for player in range(self.n_players):
            for card in self.board[player]:
                card.end_game_effect(self, player)
            for stage in range(self.wonder_stages[player]):
                self.wonders[player].stages[stage].end_game_effect(self, player)
            self.points[player] += self.scientific_symbols[player].points()
            self.points[player] += floor(self.coins[player] / 3)
            self.points[player] += sum(self.tokens[player])
        winner_score = max([(self.points[player], self.coins[player])
                            for player in range(self.n_players)])
        return [player for player in range(self.n_players)
                if (self.points[player], self.coins[player]) == winner_score]

    def pay_options(self, player: int, cost: Resources) -> "set[tuple[int][int]]":
        result = set()
        if self.coins[player] < cost.coins:
            return result
        for resources in self.resources[player]:
            for untradable in self.untradable_resources[player]:
                have = resources + untradable
                if cost <= have:
                    return {self.FREE_OPTION}
                need_to_buy = cost - have
                for resources_l in self.resources[self.left(player)]:
                    for resources_r in self.resources[self.right(player)]:
                        if need_to_buy > resources_l + resources_r:
                            continue
                        max_raw_left = sum([min(to_buy, left_has)
                                            for to_buy, left_has in zip(need_to_buy.raw(),
                                                                        resources_l.raw())])
                        max_refined_left = sum([min(to_buy, left_has)
                                                for to_buy, left_has in zip(need_to_buy.refined(),
                                                                            resources_l.refined())])

                        max_raw_right = sum([min(to_buy, right_has)
                                             for to_buy, right_has in zip(need_to_buy.raw(),
                                                                          resources_r.raw())])
                        max_refined_right = sum([min(to_buy, right_has)
                                                 for to_buy, right_has in zip(need_to_buy.refined(),
                                                                              resources_r.refined())])

                        result.update([(raw_l * self.raw_costs[player][0]\
                                        + ref_l * self.refined_costs[player][0],
                                        (need_to_buy.raw_cnt() - raw_l) * self.raw_costs[player][1]\
                                        + (need_to_buy.refined_cnt() - ref_l) * self.refined_costs[player][1])
                                       for raw_l in range(need_to_buy.raw_cnt() - max_raw_right,
                                                          max_raw_left + 1)
                                       for ref_l in range(need_to_buy.refined_cnt() - max_refined_right,
                                                          max_refined_left + 1)])
        coins_to_trade = self.coins[player] - cost.coins
        minimal_cost = max(0, sum(min(result, key=lambda payments: sum(payments),
                                      default=self.FREE_OPTION)))
        if minimal_cost > coins_to_trade:
            return set()
        return set(filter(lambda payments: sum(payments) <= minimal_cost, result))

    def chains(self, player: int) -> list:
        return [chain for card in self.board[player] for chain in card.chains]

    def moves(self, player: int) -> "list[Move]":
        if player == self.free_card_player:
            return [Move('play', d_card, (self.SPECIAL_DISCARD, self.SPECIAL_DISCARD)) 
                    for d_card in self.discard_pile 
                    if d_card.name not in [card.name for card in self.board[player]]]
        result = []
        player_chains = self.chains(player)
        for card in self.hand[player]:
            if card.name in player_chains:
                result.append(Move('play', card, self.FREE_OPTION))
            else:
                pay_options = self.pay_options(player, card.cost)
                for option in pay_options:
                    result.append(Move('play', card, option))
            
            for power, ready in self.special_powers[player]:
                if power == 'free_card_per_age' and ready:
                    result.append(Move('play', card, (self.SPECIAL_OLYPMIA, self.SPECIAL_OLYPMIA)))
            result.append(Move('sell', card, self.FREE_OPTION))
        stages_built = self.wonder_stages[player]
        if stages_built < self.wonders[player].n_stages:
            pay_options = self.pay_options(player, self.wonders[player].stages[stages_built].cost)
            for option in pay_options:
                for card in self.hand[player]:
                    result.append(Move('build_wonder', card, option))
        return list(filter(lambda move: move.type != 'play'\
                                or move.card.name not in\
                                [card.name for card in self.board[player]],
                            result))

    def play_card(self, card: Card, player: int, pay_option: "tuple[int][int]") -> None:
        if pay_option[0] == self.SPECIAL_OLYPMIA or pay_option[1] == self.SPECIAL_OLYPMIA:
            for i, (power, ready) in enumerate(self.special_powers[player]):
                if power == 'free_card_per_age':
                    self.special_powers[player][i] = ('free_card_per_age', USED)
                    break
        elif pay_option[0] == self.SPECIAL_DISCARD or pay_option[1] == self.SPECIAL_DISCARD:
            self.discard_pile.remove(card)
            self.free_card_player = None
        else:
            self.coins[player] -= card.cost.coins
            self.coins[player] -= sum(pay_option)
            self.coins[self.left(player)] += pay_option[0]
            self.coins[self.right(player)] += pay_option[1]
        self.board[player].add(card)
        self.actions_queue.append((card.immediate_effect, player))

    def sell_card(self, card: Card, player: int) -> None:
        self.discard_pile.append(card)
        self.coins[player] += 3

    def build_wonder(self, player: int, pay_option: "tuple[int][int]") -> None:
        self.coins[player] -= self.wonders[player].stages[self.wonder_stages[player]].cost.coins
        self.coins[player] -= sum(pay_option)
        self.coins[self.left(player)] += pay_option[0]
        self.coins[self.right(player)] += pay_option[1]
        self.actions_queue.append(
            (self.wonders[player].stages[self.wonder_stages[player]].immediate_effect, player))
        self.wonder_stages[player] += 1

    def do_move(self, player: int, move: Move, player_name: str='') -> None:
        if self.verbose:
            print(f'{player_name} does {move}')
        assert(move in self.moves(player))
        if move.type == 'play':
            self.play_card(move.card, player, move.pay_option)
        if move.type == 'sell':
            self.sell_card(move.card, player)
        if move.type == 'build_wonder':
            self.build_wonder(player, move.pay_option)
        if move.card in self.hand[player]:
            self.hand[player].remove(move.card)


    def resolve_actions(self, player_names: "list[str]"='') -> None:
        for action, player in self.actions_queue:
            action(self, player)
        self.actions_queue = []

        for player in range(self.n_players):
            # handle play_last_card power
            if len(self.hand[player]) == 1:
                last_card = self.hand[player][0]
                discard_last_card = True
                for power, ready in self.special_powers[player]:
                    if power == 'play_last_card':
                        discard_last_card = False
                if discard_last_card:
                    self.discard_pile.append(last_card)
                    self.hand[player].remove(last_card)

            # handle free_card_from_discard power
            for i, (power, ready) in enumerate(self.special_powers[player]):
                if power == 'free_card_from_discard' and ready:
                    self.special_powers[player][i] = ('free_card_from_discard', USED)
                    self.free_card_player = player
                    if not self.moves(player):
                        self.free_card_player = None

        if self.verbose:
            for player in range(self.n_players):
                print()
                print(f'{player_names[player]}:')
                print(f'cards built: {self.board[player]}')
                print('resources options: ')
                for resource_option in self.resources[player]:
                    print(resource_option)
                print(f'{self.coins[player]} coins')
                print((f'{self.shields[player]} shields, '
                       f'victory tokens: {self.tokens[player]}'))
                print((f'wonder {self.wonders[player].name}, '
                       f'{self.wonder_stages[player]} stages built'))
            print()


    


