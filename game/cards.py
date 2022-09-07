from base import *
from effects import *


CARDS = {
    Card(
        'lumber_yard',
        1,
        'brown',
        Resources(),
        resource_effect(Resources(wood=1)),
        no_effect,
        (),
        (3, 4)
    ),
    Card(
        'stone_pit',
        1,
        'brown',
        Resources(),
        resource_effect(Resources(stone=1)),
        no_effect,
        (),
        (3, 5)
    ),
    Card(
        'clay_pool',
        1,
        'brown',
        Resources(),
        resource_effect(Resources(clay=1)),
        no_effect,
        (),
        (3, 5)
    ),
    Card(
        'ore_vein',
        1,
        'brown',
        Resources(),
        resource_effect(Resources(ore=1)),
        no_effect,
        (),
        (3, 4)
    ),
    Card(
        'tree_farm',
        1,
        'brown',
        Resources(coins=1),
        exclusive_resources_effect(Resources(wood=1), Resources(clay=1)),
        no_effect,
        (),
        (6,)
    ),
    Card(
        'excavation',
        1,
        'brown',
        Resources(coins=1),
        exclusive_resources_effect(Resources(stone=1), Resources(clay=1)),
        no_effect,
        (),
        (4,)
    ),
    Card(
        'clay_pit',
        1,
        'brown',
        Resources(coins=1),
        exclusive_resources_effect(Resources(clay=1), Resources(ore=1)),
        no_effect,
        (),
        (3,)
    ),
    Card(
        'timber_yard',
        1,
        'brown',
        Resources(coins=1),
        exclusive_resources_effect(Resources(stone=1), Resources(wood=1)),
        no_effect,
        (),
        (3,)
    ),
    Card(
        'forest_cave',
        1,
        'brown',
        Resources(coins=1),
        exclusive_resources_effect(Resources(wood=1), Resources(ore=1)),
        no_effect,
        (),
        (5,)
    ),
    Card(
        'mine',
        1,
        'brown',
        Resources(coins=1),
        exclusive_resources_effect(Resources(ore=1), Resources(stone=1)),
        no_effect,
        (),
        (6,)
    ),
    Card(
        'loom',
        1,
        'gray',
        Resources(),
        resource_effect(Resources(textiles=1)),
        no_effect,
        (),
        (3, 6)
    ),
    Card(
        'glassworks',
        1,
        'gray',
        Resources(),
        resource_effect(Resources(glass=1)),
        no_effect,
        (),
        (3, 6)
    ),
    Card(
        'press',
        1,
        'gray',
        Resources(),
        resource_effect(Resources(papyrus=1)),
        no_effect,
        (),
        (3, 6)
    ),
    Card(
        'sawmill',
        2,
        'brown',
        Resources(coins=1),
        resource_effect(Resources(wood=2)),
        no_effect,
        (),
        (3, 4)
    ),
    Card(
        'quarry',
        2,
        'brown',
        Resources(coins=1),
        resource_effect(Resources(stone=2)),
        no_effect,
        (),
        (3, 4)
    ),
    Card(
        'brickyard',
        2,
        'brown',
        Resources(coins=1),
        resource_effect(Resources(clay=2)),
        no_effect,
        (),
        (3, 4)
    ),
    Card(
        'foundry',
        2,
        'brown',
        Resources(coins=1),
        resource_effect(Resources(ore=2)),
        no_effect,
        (),
        (3, 4)
    ),
    Card(
        'loom',
        2,
        'gray',
        Resources(),
        resource_effect(Resources(textiles=1)),
        no_effect,
        (),
        (3, 5)
    ),
    Card(
        'glassworks',
        2,
        'gray',
        Resources(),
        resource_effect(Resources(glass=1)),
        no_effect,
        (),
        (3, 5)
    ),
    Card(
        'press',
        2,
        'gray',
        Resources(),
        resource_effect(Resources(papyrus=1)),
        no_effect,
        (),
        (3, 5)
    ),
    Card(
        'workers_guild',
        3,
        'guild',
        Resources(ore=2, clay=1, stone=1, wood=1),
        no_effect,
        neighbours_cards_points_effect('brown'),
        (),
        (3,)
    ),
    Card(
        'craftsmens_guild',
        3,
        'guild',
        Resources(ore=2, stone=2),
        no_effect,
        neighbours_cards_points_effect('gray'),
        (),
        (3,)
    ),
    Card(
        'traders_guild',
        3,
        'guild',
        Resources(textiles=1, papyrus=1, glass=1),
        no_effect,
        neighbours_cards_points_effect('yellow'),
        (),
        (3,)
    ),
    Card(
        'philosophers_guild',
        3,
        'guild',
        Resources(clay=3, textiles=1, papyrus=1),
        no_effect,
        neighbours_cards_points_effect('green'),
        (),
        (3,)
    ),
    Card(
        'spies_guild',
        3,
        'guild',
        Resources(clay=3, glass=1),
        no_effect,
        neighbours_cards_points_effect('red'),
        (),
        (3,)
    ),
    Card(
        'strategists_guild',
        3,
        'guild',
        Resources(ore=2, stone=1, textiles=1),
        no_effect,
        strategists_guild_effect,
        (),
        (3,)
    ),
    Card(
        'shipowners_guild',
        3,
        'guild',
        Resources(wood=3, papyrus=1, glass=1),
        no_effect,
        combine_effects(
            your_cards_points_effect('brown', 1),
            your_cards_points_effect('gray', 1),
            your_cards_points_effect('guild', 1)
        ),
        (),
        (3,)
    ),
    Card(
        'scientists_guild',
        3,
        'guild',
        Resources(wood=2, ore=2, papyrus=1),
        no_effect,
        scientists_guild_effect,
        (),
        (3,)
    ),
    Card(
        'magistrates_guild',
        3,
        'guild',
        Resources(wood=3, stone=1, textiles=1),
        no_effect,
        neighbours_cards_points_effect('blue'),
        (),
        (3,)
    ),
    Card(
        'builders_guild',
        3,
        'guild',
        Resources(stone=2, clay=2, glass=1),
        no_effect,
        builders_guild_effect,
        (),
        (3,)
    ),
    Card(
        'pawnshop',
        1,
        'blue',
        Resources(),
        no_effect,
        points_effect(3),
        (),
        (4, 7)
    ),
    Card(
        'baths',
        1,
        'blue',
        Resources(stone=1),
        no_effect,
        points_effect(3),
        ('aqueduct',),
        (3, 7)
    ),
    Card(
        'altar',
        1,
        'blue',
        Resources(),
        no_effect,
        points_effect(2),
        ('temple',),
        (3, 5)
    ),
    Card(
        'theater',
        1,
        'blue',
        Resources(),
        no_effect,
        points_effect(2),
        ('statue',),
        (3, 6)
    ),
    Card(
        'aqueduct',
        2,
        'blue',
        Resources(stone=3),
        no_effect,
        points_effect(5),
        (),
        (3, 7)
    ),
    Card(
        'temple',
        2,
        'blue',
        Resources(wood=1, clay=1, glass=1),
        no_effect,
        points_effect(3),
        ('pantheon',),
        (3, 6)
    ),
    Card(
        'statue',
        2,
        'blue',
        Resources(wood=1, ore=2),
        no_effect,
        points_effect(4),
        ('gardens',),
        (3, 7)
    ),
    Card(
        'pantheon',
        3,
        'blue',
        Resources(clay=2, ore=1, papyrus=1, textiles=1, glass=1),
        no_effect,
        points_effect(7),
        (),
        (3, 6)
    ),
    Card(
        'gardens',
        3,
        'blue',
        Resources(wood=1, clay=2),
        no_effect,
        points_effect(5),
        (),
        (3, 4)
    ),
    Card(
        'town_hall',
        3,
        'blue',
        Resources(ore=1, stone=2, glass=1),
        no_effect,
        points_effect(6),
        (),
        (3, 5, 6)
    ),
    Card(
        'palace',
        3,
        'blue',
        Resources(clay=1, wood=1, ore=1, stone=1, glass=1, papyrus=1, textiles=1),
        no_effect,
        points_effect(8),
        (),
        (3, 7)
    ),
    Card(
        'tavern',
        1,
        'yellow',
        Resources(),
        coins_effect(5),
        no_effect,
        (),
        (4, 5, 7)
    ),
    Card(
        'east_trading_post',
        1,
        'yellow',
        Resources(),
        trading_post_effect(1),
        no_effect,
        ('forum',),
        (3, 7)
    ),
    Card(
        'west_trading_post',
        1,
        'yellow',
        Resources(),
        trading_post_effect(0),
        no_effect,
        ('forum',),
        (3, 7)
    ),
    Card(
        'marketplace',
        1,
        'yellow',
        Resources(),
        marketplace_effect,
        no_effect,
        ('caravansery',),
        (3, 6)
    ),
    Card(
        'forum',
        2,
        'yellow',
        Resources(clay=2),
        untradable_resources_effect(
            Resources(textiles=1),
            Resources(glass=1),
            Resources(papyrus=1)
        ),
        no_effect,
        ('haven',),
        (3, 6, 7)
    ),
    Card(
        'caravansery',
        2,
        'yellow',
        Resources(wood=2),
        untradable_resources_effect(
            Resources(clay=1),
            Resources(stone=1),
            Resources(ore=1),
            Resources(wood=1)
        ),
        no_effect,
        ('lighthouse',),
        (3, 5, 6)
    ),
    Card(
        'vineyard',
        2,
        'yellow',
        Resources(),
        vineyard_effect,
        no_effect,
        (),
        (3, 6)
    ),
    Card(
        'bazar',
        2,
        'yellow',
        Resources(),
        bazar_effect,
        no_effect,
        (),
        (4, 7)
    ),
    Card(
        'haven',
        3,
        'yellow',
        Resources(ore=1, wood=1, textiles=1),
        your_cards_coins_effect('brown', 1),
        your_cards_points_effect('brown', 1),
        (),
        (3, 4)
    ),
    Card(
        'lighthouse',
        3,
        'yellow',
        Resources(stone=1, glass=1),
        your_cards_coins_effect('yellow', 1),
        your_cards_points_effect('yellow', 1),
        (),
        (3, 6)
    ),
    Card(
        'chamber_of_commerce',
        3,
        'yellow',
        Resources(clay=2, papyrus=1),
        your_cards_coins_effect('gray', 2),
        your_cards_points_effect('gray', 2),
        (),
        (4, 6)
    ),
    Card(
        'stockade',
        1,
        'red',
        Resources(wood=1),
        shields_effect(1),
        no_effect,
        (),
        (3, 7)
    ),
    Card(
        'barracks',
        1,
        'red',
        Resources(ore=1),
        shields_effect(1),
        no_effect,
        (),
        (3, 5)
    ),
    Card(
        'guard_tower',
        1,
        'red',
        Resources(clay=1),
        shields_effect(1),
        no_effect,
        (),
        (3, 4)
    ),
    Card(
        'walls',
        2,
        'red',
        Resources(stone=3),
        shields_effect(2),
        no_effect,
        ('fortifications',),
        (3, 7)
    ),
    Card(
        'training_ground',
        2,
        'red',
        Resources(wood=1, ore=2),
        shields_effect(2),
        no_effect,
        ('circus',),
        (4, 6, 7)
    ),
    Card(
        'fortifications',
        3,
        'red',
        Resources(stone=1, ore=3),
        shields_effect(3),
        no_effect,
        (),
        (3, 7)
    ),
    Card(
        'circus',
        3,
        'red',
        Resources(stone=3, ore=1),
        shields_effect(3),
        no_effect,
        (),
        (4, 5, 6)
    ),
    Card(
        'arsenal',
        3,
        'red',
        Resources(ore=1, wood=2, textiles=1),
        shields_effect(3),
        no_effect,
        (),
        (3, 4, 7)
    ),
    Card(
        'apothecary',
        1,
        'green',
        Resources(textiles=1),
        scientific_symbol_effect(ScientificSymbols(compass=1)),
        no_effect,
        ('stables', 'dispensary'),
        (3, 5)
    ),
    Card(
        'workshop',
        1,
        'green',
        Resources(glass=1),
        scientific_symbol_effect(ScientificSymbols(cog=1)),
        no_effect,
        ('archery_range', 'laboratory'),
        (3, 7)
    ),
    Card(
        'scriptorium',
        1,
        'green',
        Resources(papyrus=1),
        scientific_symbol_effect(ScientificSymbols(slate=1)),
        no_effect,
        ('courthouse', 'library'),
        (3, 4)
    ),
    Card(
        'stables',
        2,
        'red',
        Resources(ore=1, clay=1, wood=1),
        shields_effect(2),
        no_effect,
        (),
        (3, 5)
    ),
    Card(
        'dispensary',
        2,
        'green',
        Resources(ore=2, glass=1),
        scientific_symbol_effect(ScientificSymbols(compass=1)),
        no_effect,
        ('arena', 'lodge'),
        (3, 4)
    ),
    Card(
        'archery_range',
        2,
        'red',
        Resources(wood=2, ore=1),
        shields_effect(2),
        no_effect,
        (),
        (3, 6)
    ),
    Card(
        'laboratory',
        2,
        'green',
        Resources(clay=2, papyrus=1),
        scientific_symbol_effect(ScientificSymbols(cog=1)),
        no_effect,
        ('siege_workshop', 'observatory'),
        (3, 5)
    ),
    Card(
        'courthouse',
        2,
        'blue',
        Resources(clay=2, textiles=1),
        no_effect,
        points_effect(4),
        (),
        (3, 5)
    ),
    Card(
        'library',
        2,
        'green',
        Resources(stone=2, textiles=1),
        scientific_symbol_effect(ScientificSymbols(slate=1)),
        no_effect,
        ('senate', 'university'),
        (3, 6)
    ),
    Card(
        'school',
        2,
        'green',
        Resources(wood=1, papyrus=1),
        scientific_symbol_effect(ScientificSymbols(slate=1)),
        no_effect,
        ('academy', 'study'),
        (3, 7)
    ),
    Card(
        'arena',
        3,
        'yellow',
        Resources(ore=1, stone=2),
        arena_immediate_effect,
        arena_end_game_effect,
        (),
        (3, 5, 7)
    ),
    Card(
        'lodge',
        3,
        'green',
        Resources(clay=2, textiles=1, papyrus=1),
        scientific_symbol_effect(ScientificSymbols(compass=1)),
        no_effect,
        (),
        (3, 6)
    ),
    Card(
        'siege_workshop',
        3,
        'red',
        Resources(wood=1, clay=3),
        shields_effect(3),
        no_effect,
        (),
        (3, 5)
    ),
    Card(
        'observatory',
        3,
        'green',
        Resources(ore=2, glass=1, textiles=1),
        scientific_symbol_effect(ScientificSymbols(cog=1)),
        no_effect,
        (),
        (3, 7)
    ),
    Card(
        'senate',
        3,
        'blue',
        Resources(ore=1, stone=1, wood=2),
        no_effect,
        points_effect(6),
        (),
        (3, 5)
    ),
    Card(
        'university',
        3,
        'green',
        Resources(wood=2, papyrus=1, glass=1),
        scientific_symbol_effect(ScientificSymbols(slate=1)),
        no_effect,
        (),
        (3, 4)
    ),
    Card(
        'academy',
        3,
        'green',
        Resources(stone=3, glass=1),
        scientific_symbol_effect(ScientificSymbols(compass=1)),
        no_effect,
        (),
        (3, 7)
    ),
    Card(
        'study',
        3,
        'green',
        Resources(wood=1, papyrus=1, textiles=1),
        scientific_symbol_effect(ScientificSymbols(cog=1)),
        no_effect,
        (),
        (3, 5)
    )
}
