import argparse

from game import *
from table import play, PlayerProcess, start_player
from players.semi_random_player import *
from players.human_player import *
from players.monte_carlo_player import *
from players.score_player import *
from players.opps_player import *
from wonders import WONDERS

player_types = [
    HumanPlayer,
    SemiRandomPlayer,
    MonteCarloPlayer,
    ScorePlayer,
    OppsPlayer
]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", default=0, type=int)
    parser.add_argument("--num_games", default=10, type=int)
    parser.add_argument("--p", default=10, type=int)
    parser.add_argument("--m", default=10, type=int)
    parser.add_argument("players", nargs='+', type=int)
    args = parser.parse_args()

    n_players = len(args.players)
    human_nr = player_types.index(HumanPlayer)
    players = [PlayerProcess(player_types[args.players[nr]],
                             start_player, nr, args.p, args.m, n_players,
                             args.players[nr] == human_nr, str(nr))
               for nr in range(n_players)]
    result = play(n_players, players, args.verbose, args.num_games)
    print(result)
