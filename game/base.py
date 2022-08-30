from dataclasses import dataclass
from typing import Callable

MAX_HAND = 7
START_COINS = 3

READY = b'R'
END_GAME = b'E'
DATA = b'D'
MOVE = b'M'
INPUT = b'I'


@dataclass(frozen=True)
class Resources(object):
    # raw
    clay: int = 0
    ore: int = 0
    stone: int = 0
    wood: int = 0
    # refined
    glass: int = 0
    papyrus: int = 0
    textiles: int = 0
    # coins
    coins: int = 0

    def __le__(self, other):
        return self.clay <= other.clay and\
               self.ore <= other.ore and\
               self.stone <= other.stone and\
               self.wood <= other.wood and\
               self.glass <= other.glass and\
               self.papyrus <= other.papyrus and\
               self.textiles <= other.textiles

    def __gt__(self, other):
        return not self <= other

    def __add__(self, other):
        clay = self.clay + other.clay
        ore = self.ore + other.ore
        stone = self.stone + other.stone
        wood = self.wood + other.wood
        glass = self.glass + other.glass
        papyrus = self.papyrus + other.papyrus
        textiles = self.textiles + other.textiles
        coins = self.coins + other.coins
        return Resources(clay, ore, stone, wood, glass, papyrus, textiles, coins)

    def __sub__(self, other):
        clay = max(self.clay - other.clay, 0)
        ore = max(self.ore - other.ore, 0)
        stone = max(self.stone - other.stone, 0)
        wood = max(self.wood - other.wood, 0)
        glass = max(self.glass - other.glass, 0)
        papyrus = max(self.papyrus - other.papyrus, 0)
        textiles = max(self.textiles - other.textiles, 0)
        coins = max(self.coins - other.coins, 0)
        return Resources(clay, ore, stone, wood, glass, papyrus, textiles, coins)

    def raw(self):
        return (self.clay, self.ore, self.stone, self.wood)

    def refined(self):
        return (self.glass, self.papyrus, self.textiles)

    def raw_cnt(self):
        return self.clay + self.ore + self.stone + self.wood

    def refined_cnt(self):
        return self.glass + self.papyrus + self.textiles

    def cnt(self):
        return self.raw_cnt() + self.refined_cnt()

@dataclass(frozen=True, eq=False)
class Card(object):
    name: str
    age: int
    colour: str
    cost: Resources
    immediate_effect: Callable
    end_game_effect: Callable
    chains: "tuple[str]"
    copies: "tuple[int]"

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        return type(self) == type(other) and self.name == other.name\
               and self.age == other.age

    def __hash__(self) -> int:
        return hash((self.name, self.age))


@dataclass(frozen=True)
class WonderStage(object):
    cost: Resources
    immediate_effect: Callable
    end_game_effect: Callable


@dataclass(frozen=True)
class Wonder(object):
    name: str
    starting_resource: Resources
    n_stages: int
    stages: "tuple[WonderStage]"

    def __repr__(self) -> str:
        return self.name


@dataclass
class ScientificSymbols(object):
    slate: int = 0
    cog: int = 0
    compass: int = 0

    def __add__(self, other):
        return ScientificSymbols(
                   self.slate + other.slate,
                   self.cog + other.cog,
                   self.compass + other.compass
               )

    def cnt(self) -> int:
        return self.slate + self.cog + self.compass

    def points(self) -> int:
        return self.slate**2 + self.cog**2 + self.compass**2\
               + 7 * min(self.slate, self.cog, self.compass)
