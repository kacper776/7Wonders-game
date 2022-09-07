import argparse

from game import *
from table import play, PlayerProcess, start_player
from players.semi_random_player import *
from players.human_player import *
from players.monte_carlo_player import *
from players.score_player import *
from players.opps_player import *
from players.training_players.training_player0 import *
from players.training_players.training_player1 import *
from players.training_players.training_player2 import *
from players.training_players.training_player3 import *
from players.brazilian_player import *

player_types = [
    HumanPlayer,
    SemiRandomPlayer,
    MonteCarloPlayer,
    ScorePlayer,
    OppsPlayer,
    BrazilianPlayer,
    TrainingPlayer0,
    TrainingPlayer1,
    TrainingPlayer2,
    TrainingPlayer3,
]


def play_with_args(args) -> "dict[str][int]":
    if len(args.players) > 7 or len(args.players) < 3:
        print(f'Invalid number of players: {len(args.players)}')
        exit(0)

    human_nr = player_types.index(HumanPlayer)
    humans = len([nr for nr in args.players if nr == human_nr])
    if humans > 1:
        print('Error: Maxiumum of 1 human player')
        exit(0)
    
    if args.num_games <= 0:
        print('Error: Non-positive number of games')
        exit(0)

    if args.p <= 0:
        print('Error: Non-positive prepare time limit')
        exit(0)

    if args.m <= 0:
        print('Error: Non-positive move time limit')
        exit(0)

    for i in args.players:
        if i < 0 or i >= len(player_types):
            print(f'Error: Unknown player type {i}')
            exit(0)

    if humans:
        args.verbose = 1
    n_players = len(args.players)
    player_names = [player_types[nr].__name__ for nr in args.players]
    for i, name in enumerate(reversed(player_names)):
        idx = n_players - 1 - i
        suffix = 0
        for j, name2 in enumerate(player_names):
            if name == name2 and idx > j:
                suffix += 1
        player_names[idx] = player_names[idx] + f'_{suffix}'

    players = [PlayerProcess(player_types[args.players[nr]],
                             start_player, nr, args.p, args.m, n_players,
                             args.players[nr] == human_nr, player_names[nr])
               for nr in range(n_players)]
    result = play(n_players, players, args.verbose, args.num_games)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", default=0, type=int)
    parser.add_argument("--num_games", default=10, type=int)
    parser.add_argument("--p", default=10, type=int)
    parser.add_argument("--m", default=200, type=int)
    parser.add_argument("players", nargs='+', type=int)
    args = parser.parse_args()
    print(play_with_args(args))
