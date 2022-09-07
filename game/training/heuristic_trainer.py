
from random import uniform

from game import *
from main import play_with_args, player_types
from players.score_player import ScorePlayer
from players.training_players.training_player0 import TrainingPlayer0
from players.training_players.training_player1 import TrainingPlayer1
from players.training_players.training_player2 import TrainingPlayer2
import training.heuristic_for_training0
import training.heuristic_for_training1
import training.heuristic_for_training2
import heuristics

class game_args(object):
    def __init__(self, num_games: int, players: "list[int]",
                 verbose: int=0, p: int=10, m: int=200) -> None:
        self.num_games = num_games
        self.players = players
        self.verbose = verbose
        self.p = p
        self.m = m

single_coeff = [
    'CAN_PLAY_CARD',
    'CAN_BUILD_WONDER',
    'RAW',
    'REFINED',
    'DISC_RAW',
    'DISC_REFINED',
    'COIN_SCORE',
]

age_coeff = [
    'WIN_SCORE',
    'SCIENCE_BONUS'
]

LEARNING_RATE = 0.25

default_players = [
    player_types.index(ScorePlayer),
    player_types.index(TrainingPlayer0),
    player_types.index(TrainingPlayer1),
    player_types.index(TrainingPlayer2)
]
default_args = game_args(30, default_players)

def random_change():
    return uniform(-LEARNING_RATE, LEARNING_RATE)

def change_coefficients(training_agent):
    for coeff in single_coeff:
        # change = choice(range(-2, 3)) * 0.05
        new_value = getattr(heuristics, coeff) + random_change()
        setattr(training_agent, coeff, new_value)
    for coeff in age_coeff:
        value = getattr(heuristics, coeff)
        new_value = []
        for age in range(3):
            new_value.append(value[age] + random_change())
        setattr(training_agent, coeff, new_value)

agents = [training.heuristic_for_training0,
          training.heuristic_for_training1,
          training.heuristic_for_training2]

for i in range(240):
    print(f'----------------- iteraton {i} -----------------')
    for agent in agents:
        change_coefficients(agent)
    result = play_with_args(default_args)
    print(result)
    weights = [0] * 3
    for suffix in range(3):
        for name, res in result.items():
            if name.endswith(f'{str(suffix)}_0'):
                weights[suffix] += res
    
    for coeff in single_coeff:
        new_coeff = sum([getattr(agent, coeff) * weights[i]
                         for i, agent in enumerate(agents)]) / sum(weights)
        setattr(heuristics, coeff, new_coeff)
    for coeff in age_coeff:
        new_coeff = []
        for age in range(3):
            new_coeff.append(sum([getattr(agent, coeff)[age] * weights[i]
                                  for i, agent in enumerate(agents)]) / sum(weights))
        setattr(heuristics, coeff, new_coeff)
    print('current coefficients:')
    for coeff in single_coeff + age_coeff:
        print(f'{coeff}: {getattr(heuristics, coeff)}')

    

for coeff in single_coeff + age_coeff:
    print(f'{coeff}: {getattr(heuristics, coeff)}')

