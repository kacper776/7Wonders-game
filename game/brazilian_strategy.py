from base import *
from game import *

def qt_civilian_structure(game: SevenWonders, nr: int):
    return len([card for card in game.hand[nr]
                if card.colour == 'blue'])


def qt_commercial_structure(game: SevenWonders, nr: int):
    return len([card for card in game.hand[nr]
                if card.colour == 'yellow'])


def qt_military_structure(game: SevenWonders, nr: int):
    return len([card for card in game.hand[nr]
                if card.colour == 'red'])


def qt_scientific_structure(game: SevenWonders, nr: int):
    return len([card for card in game.hand[nr]
                if card.colour == 'green'])


def qt_trading_post(game: SevenWonders, nr: int):
    return len([card for card in game.hand[nr]
                if card.name.endswith('trading_post')])
    

def qt_shields(game: SevenWonders, nr: int):
    return game.shields[nr]


def lumber_yard(game: SevenWonders, nr: int):
    amount_raw_material = game.resources[nr][0].raw_cnt()

    # Wonder: ALEXANDRIA B(12) Is important to play 1 Wood card and unlock the first stage
    if game.wonders[nr].name == 'alexandria(B)':
        return 4

    # Wonder: GIZA B(7) unlock the 1st stage
    if game.wonders[nr].name == 'gizah(B)':
        return 4

    # Wonder:  OLYMPIA A(2) build your 1st stage
    if game.wonders[nr].name == 'olympia(A)':
        return 5

    # Monopoly of wood
    if amount_raw_material < 2:
        return 4

    return 1


def stone_pit(game: SevenWonders, nr: int):
    amount_raw_material = game.resources[nr][0].raw_cnt()

    # Wonder: GIZA B(7) unlock the 2nd stage
    if game.wonders[nr].name == 'gizah(B)':
        return 3

    # Wonder:  OLYMPIA A(2) build the 2nd stage
    if game.wonders[nr].name == 'olympia(A)':
        return 4

    # Wonder: RHODOS B(10) neighbors logic
    # if gizah isn't present
    if not game.wonders[game.left(nr)].name.startswith('gizah') and\
       not game.wonders[game.right(nr)].name.startswith('gizah'):
        return 1

    if amount_raw_material < 2:
        return 3

    return 1


def clay_pool(game: SevenWonders, nr: int):
    amount_raw_material = game.resources[nr][0].raw_cnt()
    clay = max([option.clay for option in game.resources[nr]])

    # Wonder: ALEXANDRIA B(12) Is important to play 1 Clay card and unlock the first stage
    if game.wonders[nr].name == 'alexandria(B)':
        return 4

    # Wonder: BABYLON B(8)
    if game.wonders[nr].name == 'babylon(B)':
        if clay < 2:
            return 3

    # Wonder: GIZA B(7) unlock the 3rd stage
    if game.wonders[nr].name == 'gizah(B)':
        return 2

    # Wonder: HALIKARNASSOS B(13) unlock your 2nd stage
    if game.wonders[nr].name == 'halikarnassos(B)':
        return 4

    if amount_raw_material < 2:
        return 3

    return 1


def ore_vein(game: SevenWonders, nr: int):
    amount_raw_material = game.resources[nr][0].raw_cnt()

    # Wonder: OLYMPIA A(2) build the 3rd stage
    if game.wonders[nr].name == 'olympia(A)':
        return 3

    # Wonder: HALIKARNASSOS B(13) unlock your 1nd stage
    if game.wonders[nr].name == 'halikarnassos(B)':
        return 3

    if amount_raw_material < 2:
        return 3

    return 1


def three_farm(game: SevenWonders, nr: int):
    amount_raw_material = game.resources[nr][0].raw_cnt()

    # Wonder: GIZA B(7) unlock 2 stages of your wonder
    if game.wonders[nr].name == 'gizah(B)':
        return 5

    if amount_raw_material < 2:
        return 3

    return 1


def excavation(game: SevenWonders, nr: int):
    amount_raw_material = game.resources[nr][0].raw_cnt()

    if amount_raw_material < 2:
        return 3

    return 1


def clay_pit(game: SevenWonders, nr: int):
    clay = max([option.clay for option in game.resources[nr]])

    # Wonder: BABYLON B(8)
    if game.wonders[nr].name == 'babylon(B)':
        if clay < 2:
            return 3

    # Wonder: HALIKARNASSOS B(13) you need both resources to build your stages
    if game.wonders[nr].name == 'halikarnassos(B)':
        return 5

    # starts with Rhodes or Babylon ?
    if game.age > 1 or (game.wonders[nr].name.startswith('rhodos') or
                        game.wonders[nr].name.startswith('babylon')):
        return 3

    return 5


def timber_yard(game: SevenWonders, nr: int):
    amount_raw_material = game.resources[nr][0].raw_cnt()

    # starts with Rhodes or Babylon ?
    if (game.wonders[nr].name.startswith('rhodos') or
         game.wonders[nr].name.startswith('babylon')):
        return 5

    if amount_raw_material < 3:
        return 3

    return 1


def forest_cave(game: SevenWonders, nr: int):
    amount_raw_material = game.resources[nr][0].raw_cnt()

    if amount_raw_material < 2:
        return 3

    return 1


def mine(game: SevenWonders, nr: int):
    amount_raw_material = game.resources[nr][0].raw_cnt()

    if amount_raw_material < 2:
        return 3

    return 1


def sawmill(game: SevenWonders, nr: int):
    amount_wood = max([option.wood for option in game.resources[nr]])

    # Wonder: EPHESOS B(11) monopoly of wood
    if game.wonders[nr].name == 'ephesos(B)':
        return 2

    # Wonder: ALEXANDRIA B(12) Is important to play 1 Clay card and unlock the first stage
    if game.wonders[nr].name == 'alexandria(B)':
        if amount_wood < 1:
            return 4
        else:
            return 2

    # Wonder: BABYLON B(8) your 2nd wonder needs and you can do the monopoly
    if game.wonders[nr].name == 'babylon(B)':
        return 4

    # Wonder: GIZA B(7) unlock the 3rd stage
    if game.wonders[nr].name == 'gizah(B)':
        if amount_wood < 1:
            return 5

    # Wonder:  OLYMPIA A(2)
    if amount_wood < 2 and (not any([option.wood for option in game.resources[game.left(nr)]]) or\
                            not any([option.wood for option in game.resources[game.right(nr)]]) or\
                            game.coins[nr] == 0):
        return 3

    # Wonder: RHODOS B(10) neighbors logic
    # if gizah isn't present
    if not game.wonders[game.left(nr)].name.startswith('gizah') and\
       not game.wonders[game.right(nr)].name.startswith('gizah'):
        return 5

    if amount_wood < 2:
        return 2

    return 1


def quarry(game: SevenWonders, nr: int):
    amount_stone = max([option.stone for option in game.resources[nr]])

    # Wonder: ALEXANDRIA B(12) Is important to play 1 Clay card and unlock the first stage
    if game.wonders[nr].name == 'alexandria(B)':
        return 4

    # Wonder: BABYLON B(8) allows to try to pick some cards like: Wall | Tablet | Compass
    if game.wonders[nr].name == 'babylon(B)':
        return 3

    # Wonder: RHODOS B(10) allows to try to pick some cards like: Wall | Tablet | Compass
    if game.wonders[nr].name == 'babylon(B)':
        return 5

    # Wonder: GIZA B(7) unlock the 3rd stage
    if game.wonders[nr].name == 'gizah(B)':
        if amount_stone < 2:
            return 3
        elif amount_stone < 1:
            return 4

    # Wonder:  OLYMPIA A(2)
    if game.wonders[nr].name == 'olympia(A)':
        if amount_stone < 2:
            return 4

    # Wonder: HALIKARNASSOS B(13) unlock your 1nd stage
    if game.wonders[nr].name == 'halikarnassos(B)':
        return 3

    # Pay attention to this card so you can build Wall
    return 2


def brickyard(game: SevenWonders, nr: int):
    amount_clay = max([option.clay for option in game.resources[nr]])

    # Wonder: EPHESOS B(11) gives you: Gear | Forum for free.
    if game.wonders[nr].name == 'ephesos(B)':
        return 3

    # Wonder: BABYLON B(8) allows to try to pick some cards like: Wall | Tablet | Compass
    if game.wonders[nr].name == 'babylon(B)':
        if amount_clay < 2:
            return 3

    # Wonder: GIZA B(7) unlock the 3rd stage
    if game.wonders[nr].name == 'gizah(B)':
        if amount_clay < 2:
            return 2
        elif amount_clay < 1:
            return 3

    # Wonder: HALIKARNASSOS B(13) unlock your 1nd stage
    if game.wonders[nr].name == 'halikarnassos(B)':
        if amount_clay < 2:
            return 4
        elif amount_clay < 1:
            return 5

    return 1


def foundry(game: SevenWonders, nr: int):
    amount_ore = max([option.ore for option in game.resources[nr]])

    # Wonder: EPHESOS B(11) links very well with: Compass | Theater | Hero guild.
    if game.wonders[nr].name == 'ephesos(B)':
        return 3

    # Wonder: RHODOS B(10) you need 4x ore to build your 2nd stage
    if game.wonders[nr].name == 'babylon(B)':
        return 4

    # Wonder:  OLYMPIA A(2)
    if game.wonders[nr].name == 'olympia(A)':
        if amount_ore < 2:
            return 4

    # Wonder: HALIKARNASSOS B(13)
    if game.wonders[nr].name == 'halikarnassos(B)':
        if amount_ore < 2:
            return 2
        elif amount_ore < 1:
            return 5

    return 1


def loom(game: SevenWonders, nr: int):
    is_in_hand = len([card for card in game.hand[nr]
                      if card.name == 'marketplace']) > 0
    glass = max([option.glass for option in game.resources[nr]])
    loom = max([option.textiles for option in game.resources[nr]])

    # Wonder: EPHESOS B(11)
    if game.wonders[nr].name == 'ephesos(B)':
        if loom < 1:
            return 4

    # Wonder: BABYLON B(8)
    if game.wonders[nr].name == 'babylon(B)':
        if loom < 1:
            return 3

    # Wonder: RHODOS B(10)
    if game.wonders[nr].name == 'babylon(B)':
        if loom < 1:
            return 3

    # Wonder:  OLYMPIA A(2) you can get the compass and get a free chain to the red card Stables
    if game.wonders[nr].name == 'olympia(A)':
        if loom < 1:
            return 4

    if (not is_in_hand) and (glass < 1) and (loom < 1):
        return 4
    elif not is_in_hand:
        return 2

    return 1


def glassworks(game: SevenWonders, nr: int):
    is_in_hand = len([card for card in game.hand[nr]
                      if card.name == 'marketplace']) > 0
    glass = max([option.glass for option in game.resources[nr]])
    loom = max([option.textiles for option in game.resources[nr]])

    # Wonder: EPHESOS B(11)
    if game.wonders[nr].name == 'ephesos(B)':
        if glass < 1:
            return 4

    # Wonder: BABYLON B(8)
    if game.wonders[nr].name == 'babylon(B)':
        if glass < 1:
            return 2

    # Wonder: RHODOS B(10)
    if game.wonders[nr].name == 'babylon(B)':
        if glass < 1:
            return 3

    # Wonder: HALIKARNASSOS B(13) to build stage && play militar
    if game.wonders[nr].name == 'halikarnassos(B)':
        if glass < 1:
            return 5

    if (not is_in_hand) & (glass < 1) & (loom < 1):
        return 4

    if not is_in_hand:
        return 2

    return 1


def press(game: SevenWonders, nr: int):
    papyrus = max([option.papyrus for option in game.resources[nr]])

    # Wonder: BABYLON B(8)
    if game.wonders[nr].name == 'babylon(B)':
        if papyrus < 1:
            return 3

    # Wonder: GIZA B(7) Apart from Paper, you can freely ignore the gray resources and get a lot of brown resources
    if game.wonders[nr].name == 'gizah(B)':
        return 4

    # Wonder: HALIKARNASSOS B(13) build stage
    if game.wonders[nr].name == 'halikarnassos(B)':
        if papyrus < 1:
            return 4

    return 1


def altar(game: SevenWonders, nr: int):
    return 1


def theater(game: SevenWonders, nr: int):
    return 1


def pawnshop(game: SevenWonders, nr: int):
    return 2


def baths(game: SevenWonders, nr: int):
    return 2


def temple(game: SevenWonders, nr: int):
    count_civilian_structure = qt_civilian_structure(game)

    if count_civilian_structure < 2:
        return 3

    return 1


def courthouse(game: SevenWonders, nr: int):
    count_civilian_structure = qt_civilian_structure(game)

    if count_civilian_structure < 2:
        return 3

    return 1


def statue(game: SevenWonders, nr: int):
    count_civilian_structure = qt_civilian_structure(game)

    if count_civilian_structure < 2:
        return 3

    return 1


def aqueduct(game: SevenWonders, nr: int):
    count_civilian_structure = qt_civilian_structure(game)

    if count_civilian_structure < 2:
        return 3

    return 1


def gardens(game: SevenWonders, nr: int):
    return 3


def town_hall(game: SevenWonders, nr: int):
    return 4


def senate(game: SevenWonders, nr: int):
    return 4


def pantheon(game: SevenWonders, nr: int):
    return 5


def palace(game: SevenWonders, nr: int):
    return 5


def tavern(game: SevenWonders, nr: int):
    return 1


def east_trading_post(game: SevenWonders, nr: int):
    amount_raw_material = game.resources[nr][0].raw_cnt()
    amount_raw_material_right_neighbor = game.resources[game.right(nr)][0].raw_cnt()
    amount_raw_material_left_neighbor = game.resources[game.left(nr)][0].raw_cnt()


    west_trading_post_card = len([card for card in game.hand[nr]
                                  if card.name == 'west_trading_post']) > 0
    marketplace_card = len([card for card in game.hand[nr]
                            if card.name == 'marketplace']) > 0

    count_trading_post = qt_trading_post(game)

    # if you cannot have the brown resources && your neighbor have
    if (amount_raw_material <= 1) & \
            (amount_raw_material_right_neighbor > 1 | amount_raw_material_left_neighbor > 1):
        return 4

    # Wonder: EPHESOS B(11) regular supply of money
    if game.wonders[nr].name == 'ephesos(B)':
        return 3

    # Wonder: ALEXANDRIA B(12)
    if game.wonders[nr].name == 'alexandria(B)':
        if west_trading_post_card & marketplace_card:
            return 1
        elif west_trading_post_card | marketplace_card:
            return 4
        else:
            return 4

    # Wonder: GIZA B(7)
    if game.wonders[nr].name == 'gizah(B)':
        if count_trading_post < 1:
            return 4

    # Wonder:  OLYMPIA A(2) Trading Post continues a good card for military because you need a lot of brown resources
    if game.wonders[nr].name == 'olympia(A)':
        return 4

    # Wonder: HALIKARNASSOS B(13) Pick the Trading Post is never a bad move
    if game.wonders[nr].name == 'halikarnassos(B)':
        return 4

    return 1


def west_trading_post(game: SevenWonders, nr: int):
    amount_raw_material = game.resources[nr][0].raw_cnt()
    
    amount_raw_material_right_neighbor = game.resources[game.right(nr)][0].raw_cnt()

    amount_raw_material_left_neighbor = game.resources[game.left(nr)][0].raw_cnt()
    east_trading_post_card = "East Trading Post"
    marketplace_card = "Marketplace"

    east_trading_post_card = len([card for card in game.hand[nr]
                                  if card.name == 'east_trading_post']) > 0
    marketplace_card = len([card for card in game.hand[nr]
                            if card.name == 'marketplace']) > 0

    count_trading_post = qt_trading_post(game)

    # if you cannot have the brown resources && your neighbor have
    if (amount_raw_material <= 1) & (amount_raw_material_right_neighbor > 1\
        | amount_raw_material_left_neighbor > 1):
        return 4

    # Wonder: EPHESOS B(11) regular supply of money
    if game.wonders[nr].name == 'ephesos(B)':
        return 3

    # Wonder: ALEXANDRIA B(12)
    if game.wonders[nr].name == 'alexandria(B)':
        if east_trading_post_card & marketplace_card:
            return 1
        elif east_trading_post_card | marketplace_card:
            return 4
        else:
            return 4

    # Wonder: GIZA B(7)
    if game.wonders[nr].name == 'gizah(B)':
        if count_trading_post < 1:
            return 4

    # Wonder:  OLYMPIA A(2) Trading Post continues a good card for military because you need a lot of brown resources
    if game.wonders[nr].name == 'olympia(A)':
        return 4

    # Wonder: HALIKARNASSOS B(13) Pick the Trading Post is never a bad move
    if game.wonders[nr].name == 'halikarnassos(B)':
        return 4

    return 1


def marketplace(game: SevenWonders, nr: int):
    east_trading_post_card = "East Trading Post"
    west_trading_post_card = "West Trading Post"

    east_trading_post_card = len([card for card in game.hand[nr]
                                  if card.name == 'east_trading_post']) > 0
    west_trading_post_card = len([card for card in game.hand[nr]
                                  if card.name == 'west_trading_post']) > 0

    # Wonder: ALEXANDRIA B(12)
    if game.wonders[nr].name == 'alexandria(B)':
        if east_trading_post_card & west_trading_post_card:
            return 1
        elif east_trading_post_card | west_trading_post_card:
            return 4
        else:
            return 4

    return 4


def forum(game: SevenWonders, nr: int):
    is_in_hand = len([card for card in game.hand[nr]
                      if card.name == 'marketplace']) > 0
    glass = max([option.glass for option in game.resources[nr]])
    loom = max([option.textiles for option in game.resources[nr]])
    amount_clay = max([option.clay for option in game.resources[nr]])

    count_trading_post = qt_trading_post(game)

    # Wonder: EPHESOS B(11)
    if game.wonders[nr].name == 'ephesos(B)':
        if count_trading_post > 0 | amount_clay >= 2:
            return 5
        else:
            return 2

    # Wonder: GIZA B(7)
    if game.wonders[nr].name == 'gizah(B)':
        if count_trading_post > 0:
            return 5

    if (not is_in_hand) & (glass < 1) & (loom < 1):
        return 4

    if not is_in_hand:
        return 2

    return 1


def caravansery(game: SevenWonders, nr: int):
    return 5


def vineyard(game: SevenWonders, nr: int):
    east_trading_post_card = "East Trading Post"
    west_trading_post_card = "West Trading Post"

    east_trading_post_card = len([card for card in game.hand[nr]
                                  if card.name == 'east_trading_post']) > 0
    west_trading_post_card = len([card for card in game.hand[nr]
                                  if card.name == 'west_trading_post']) > 0

    amount_raw_material_right_neighbor = game.resources[game.right(nr)][0].raw_cnt()

    amount_raw_material_left_neighbor = game.resources[game.left(nr)][0].raw_cnt()

    # Trading Post = 1 && neighboor have a lot of raw_material
    if (east_trading_post_card | west_trading_post_card) & \
            (amount_raw_material_right_neighbor >= 4 | amount_raw_material_left_neighbor >= 4):
        return 3

    return 1


def bazar(game: SevenWonders, nr: int):
    amount_manufacture_good = max([option.papyrus for option in game.resources[nr]]) +\
                              max([option.textiles for option in game.resources[nr]]) + \
                              max([option.glass for option in game.resources[nr]])
    amount_raw_material_right_neighbor = game.resources[game.right(nr)][0].raw_cnt()
    amount_raw_material_left_neighbor = game.resources[game.left(nr)][0].raw_cnt()

    total_raw_material = amount_manufacture_good + amount_raw_material_right_neighbor\
                         + amount_raw_material_left_neighbor

    if total_raw_material >= 4:
        return 3

    return 1


def haven(game: SevenWonders, nr: int):
    amount_raw_material = game.resources[nr][0].raw_cnt()

    # Wonder: GIZA B(7) Just be sure you can pay for Textile to play the Haven
    if game.wonders[nr].name == 'gizah(B)':
        return 4

    if amount_raw_material >= 4:
        return 3

    return 1


def lighthouse(game: SevenWonders, nr: int):
    amount_of_commercial_structure = qt_commercial_structure(game)

    if amount_of_commercial_structure >= 4:
        return 3

    return 1


def chamber_of_commerce(game: SevenWonders, nr: int):
    amount_manufacture_good = max([option.papyrus for option in game.resources[nr]]) +\
                              max([option.textiles for option in game.resources[nr]]) +\
                              max([option.glass for option in game.resources[nr]])

    if amount_manufacture_good >= 2:
        return 3

    return 1


def arena(game: SevenWonders, nr: int):
    coins = max([option.papyrus for option in game.resources[nr]])
    wonder_stage = game["wonder_stage"]

    if (coins < 3) & (wonder_stage >= 1):
        return 3

    return 1


def stockade(game: SevenWonders, nr: int):
    amount_of_military_cards = qt_military_structure(game)

    if amount_of_military_cards < 2:
        return 4
    if amount_of_military_cards < 1:
        return 5

    return 1


def barracks(game: SevenWonders, nr: int):
    amount_of_military_cards = qt_military_structure(game)

    if amount_of_military_cards < 2:
        return 4
    if amount_of_military_cards < 1:
        return 5

    return 1


def guard_tower(game: SevenWonders, nr: int):
    amount_of_military_cards = qt_military_structure(game)

    if amount_of_military_cards < 2:
        return 4
    if amount_of_military_cards < 1:
        return 5

    return 1


def walls(game: SevenWonders, nr: int):
    amount_of_military_cards = qt_shields(game, nr)
    amount_military_cards_right_neighbor = qt_shields(game, game.right(nr))
    amount_military_cards_left_neighbor = qt_shields(game, game.left(nr))

    # military_structure < 1 || if you aren't the military leader
    if (amount_of_military_cards < 1) | (amount_military_cards_left_neighbor >= amount_of_military_cards) \
            | (amount_military_cards_right_neighbor >= amount_of_military_cards):
        return 5

    return 1


def training_ground(game: SevenWonders, nr: int):
    amount_of_military_cards = qt_shields(game, nr)
    amount_military_cards_right_neighbor = qt_shields(game, game.right(nr))
    amount_military_cards_left_neighbor = qt_shields(game, game.left(nr))

    # military_structure < 1 || if you aren't the military leader
    if (amount_of_military_cards < 1) | (amount_military_cards_left_neighbor >= amount_of_military_cards) \
            | (amount_military_cards_right_neighbor >= amount_of_military_cards):
        return 5

    return 1


def stables(game: SevenWonders, nr: int):
    amount_of_military_cards = qt_shields(game, nr)
    amount_military_cards_right_neighbor = qt_shields(game, game.right(nr))
    amount_military_cards_left_neighbor = qt_shields(game, game.left(nr))

    # military_structure < 1 || if you aren't the military leader
    if (amount_of_military_cards < 1) | (amount_military_cards_left_neighbor >= amount_of_military_cards) \
            | (amount_military_cards_right_neighbor >= amount_of_military_cards):
        return 5

    return 1


def archery_range(game: SevenWonders, nr: int):
    amount_of_military_cards = qt_shields(game, nr)
    amount_military_cards_right_neighbor = qt_shields(game, game.right(nr))
    amount_military_cards_left_neighbor = qt_shields(game, game.left(nr))

    # military_structure < 1 || if you aren't the military leader
    if (amount_of_military_cards < 1) | (amount_military_cards_left_neighbor >= amount_of_military_cards) \
            | (amount_military_cards_right_neighbor >= amount_of_military_cards):
        return 5

    return 1


def fortifications(game: SevenWonders, nr: int):
    amount_of_military_cards = qt_shields(game, nr)
    amount_military_cards_right_neighbor = qt_shields(game, game.right(nr))
    amount_military_cards_left_neighbor = qt_shields(game, game.left(nr))
    my_amount_plus_this_card = amount_of_military_cards + 3

    # you need this card for win?
    if (amount_of_military_cards < 1) | (amount_military_cards_left_neighbor >= amount_of_military_cards) \
            | (amount_military_cards_right_neighbor >= amount_of_military_cards):
        if(my_amount_plus_this_card >= amount_military_cards_left_neighbor) | (my_amount_plus_this_card >= amount_military_cards_right_neighbor):
            return 5

    return 1


def circus(game: SevenWonders, nr: int):
    amount_of_military_cards = qt_shields(game, nr)
    amount_military_cards_right_neighbor = qt_shields(game, game.right(nr))
    amount_military_cards_left_neighbor = qt_shields(game, game.left(nr))
    my_amount_plus_this_card = amount_of_military_cards + 3

    # you need this card for win?
    if (amount_of_military_cards < 1) | (amount_military_cards_left_neighbor >= amount_of_military_cards) \
            | (amount_military_cards_right_neighbor >= amount_of_military_cards):
        if(my_amount_plus_this_card >= amount_military_cards_left_neighbor) | (my_amount_plus_this_card >= amount_military_cards_right_neighbor):
            return 5

    return 1


def arsenal(game: SevenWonders, nr: int):
    amount_of_military_cards = qt_shields(game, nr)
    amount_military_cards_right_neighbor = qt_shields(game, game.right(nr))
    amount_military_cards_left_neighbor = qt_shields(game, game.left(nr))
    my_amount_plus_this_card = amount_of_military_cards + 3

    # you need this card for win?
    if (amount_of_military_cards < 1) | (amount_military_cards_left_neighbor >= amount_of_military_cards) \
            | (amount_military_cards_right_neighbor >= amount_of_military_cards):
        if(my_amount_plus_this_card >= amount_military_cards_left_neighbor) | (my_amount_plus_this_card >= amount_military_cards_right_neighbor):
            return 5

    return 1


def siege_workshop(game: SevenWonders, nr: int):
    amount_of_military_cards = qt_shields(game, nr)
    amount_military_cards_right_neighbor = qt_shields(game, game.right(nr))
    amount_military_cards_left_neighbor = qt_shields(game, game.left(nr))
    my_amount_plus_this_card = amount_of_military_cards + 3

    # you need this card for win?
    if (amount_of_military_cards < 1) | (amount_military_cards_left_neighbor >= amount_of_military_cards) \
            | (amount_military_cards_right_neighbor >= amount_of_military_cards):
        if(my_amount_plus_this_card >= amount_military_cards_left_neighbor) | (my_amount_plus_this_card >= amount_military_cards_right_neighbor):
            return 5

    return 1


def apothecary(game: SevenWonders, nr: int):
    return 1


def workshop(game: SevenWonders, nr: int):
    # Wonder: EPHESOS B(11)
    if game.wonders[nr].name == 'ephesos(B)':
        return 2

    return 1


def scriptorium(game: SevenWonders, nr: int):
    # Wonder: EPHESOS B(11) free Tablet
    if game.wonders[nr].name == 'ephesos(B)':
        return 5

    return 1


def dispensary(game: SevenWonders, nr: int):
    amount_ore = max([option.ore for option in game.resources[nr]])
    amount_glass = max([option.glass for option in game.resources[nr]])
    amount_scientific_structure = qt_scientific_structure(game)

    # Wonder: EPHESOS B(11) free Tablet
    if game.wonders[nr].name == 'ephesos(B)':
        if (amount_ore >= 2) & amount_glass & (amount_scientific_structure < 3):
            return 2

    return 1


def laboratory(game: SevenWonders, nr: int):
    amount_ore = max([option.ore for option in game.resources[nr]])
    amount_scientific_structure = qt_scientific_structure(game)

    # Wonder: EPHESOS B(11) free Tablet
    if game.wonders[nr].name == 'ephesos(B)':
        if (amount_ore >= 2) & (amount_scientific_structure < 3):
            return 3
        else:
            return 2

    return 1


def library(game: SevenWonders, nr: int):
    amount_stone = game["resources"]["stone"]

    # Wonder: HALIKARNASSOS B(13)
    if game.wonders[nr].name == 'halikarnassos(B)':
        if amount_stone >= 2:
            return 5

    return 1


def school(game: SevenWonders, nr: int):
    amount_scientific_structure = qt_scientific_structure(game)

    # Wonder: EPHESOS B(11) free Tablet
    if game.wonders[nr].name == 'ephesos(B)':
        if amount_scientific_structure < 2:
            return 2

    return 1


def lodge(game: SevenWonders, nr: int):
    return 1


def observatory(game: SevenWonders, nr: int):
    return 1


def university(game: SevenWonders, nr: int):
    return 1


def academy(game: SevenWonders, nr: int):
    return 1


def study(game: SevenWonders, nr: int):
    return 1


def workers_guild(game: SevenWonders, nr: int):
    return 1


def craftsmens_guild(game: SevenWonders, nr: int):
    return 1


def traders_guild(game: SevenWonders, nr: int):
    return 1


def philosophers_guild(game: SevenWonders, nr: int):
    return 1


def spies_guild(game: SevenWonders, nr: int):
    return 1


def magistrates_guild(game: SevenWonders, nr: int):
    return 1


def shipowners_guild(game: SevenWonders, nr: int):
    return 1


def strategists_guild(game: SevenWonders, nr: int):
    # Wonder: RHODOS B(10) allows to try to pick some cards like: Wall | Tablet | Compass
    if game.wonders[nr].name == 'babylon(B)':
        return 5
    return 1


def scientists_guild(game: SevenWonders, nr: int):
    coins = game["resources"]["coins"]

    # Wonder: EPHESOS B(11) free Tablet
    if game.wonders[nr].name == 'ephesos(B)':
        if coins >= 2:
            return 4

    return 1


def builders_guild(game: SevenWonders, nr: int):
    return 1
