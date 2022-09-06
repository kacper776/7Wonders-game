from copy import copy
from math import perm
from random import sample
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection
from itertools import permutations

from matplotlib import table

from base import *
from game import *
from wonders import WONDERS
from players.base_player import AbstractPlayer


class DeadPlayer(Exception):
    def __init__(self, nr: int) -> None:
        self.nr = nr



class PlayerProcess(object):
    def __init__(self, player_class: AbstractPlayer, function: Callable,
                 nr: int, prepare_time: float, move_time: float,
                 n_players: int, human: bool, name: str="") -> None:
        self.name = name
        self.nr = nr
        self.original_nr = nr
        self.human = human
        self.parent_conn, child_conn = Pipe()
        self.player_class = player_class
        self.n_players = n_players
        self.prepare_time = prepare_time
        self.move_time = move_time
        self.process = Process(target=function,
                               args=(player_class, nr, child_conn,
                                     prepare_time, move_time, n_players),
                               name=name,
                               daemon=True)
        self.process.start()

    def restart(self):
        self.parent_conn.close()
        self.parent_conn, child_conn = Pipe()
        self.process = Process(target=start_player,
                               args=(self.player_class, self.nr,
                                     child_conn, self.prepare_time,
                                     self.move_time, self.n_players),
                               name=self.name,
                               daemon=True)
        self.process.start()
        
    def send(self, message_type: bytes, message: object=None) -> None:
        self.parent_conn.send((message_type, message))

    def get(self, message_type: bytes) -> object:
        try:
            type_got, data = self.parent_conn.recv()
        except EOFError:
            raise DeadPlayer(self.nr)
        assert(type_got == message_type)
        return data

    def kill(self) -> None:
        self.parent_conn.close()
        if self.process.is_alive():
            self.process.terminate()        


def play(n_players: int, players: "list[PlayerProcess]",
         verbose: int, n_games: int) -> "list[int]":
    def send_to_all(message_type: str, message=None) -> None:
        for process in players:
            process.send(message_type, message)

    def wait_all(message) -> None:
        for process in players:
            process.get(message)

    def update_players_data(game: SevenWonders, active_players: "list[int]",
                            new_game: bool=False) -> None:
        saved_hand = [copy(game.hand[player]) for player in range(n_players)]
        saved_discard = copy(game.discard_pile)
        saved_verbose = game.verbose
        game.discard_pile = []
        game.verbose = False
        for player, process in enumerate(players):
            if player not in active_players:
                continue
            other_players = [p for p in range(n_players) if p != player]
            for other_player in other_players:
                game.hand[other_player] = None
            if new_game:
                process.send(DATA, (game, player))
            elif game.free_card_player == player:
                process.send(DATA, (game, saved_discard))
            else:
                process.send(DATA, (game, game.hand[player]))
            for other_player in other_players:
                game.hand[other_player] = saved_hand[other_player]
            game.discard_pile = saved_discard
        game.verbose = saved_verbose
            
    def do_moves(game: SevenWonders, moves: "list[tuple[int][Move][str]]") -> None:
        for player, move, name in moves:
            game.do_move(player, move, name)
        game.resolve_actions([process.name
                              for process in players])

    def rotate_hands(game: SevenWonders) -> None:
        dir = [-1, 1, -1][game.age - 1]
        saved_hand = [copy(game.hand[player]) for player in range(n_players)]
        for player in range(n_players):
            game.hand[player] = saved_hand[(player - dir + n_players) % n_players]

    def handle_free_card_from_dicard(game: SevenWonders) -> None:
        player = game.free_card_player
        update_players_data(game, [player])
        players[player].send(MOVE)
        move = players[player].get(MOVE)
        do_moves(game, [(player, move, players[player].name)])

    def play_game(game: SevenWonders) -> "list[int]":
        update_players_data(game, range(n_players), new_game=True)
        wait_all(READY)

        for age in range(1, 4):
            game.start_age(age)
            active_players = [player for player in range(n_players) if game.hand[player]]
            while active_players:
                update_players_data(game, active_players)
                for player in active_players:
                    players[player].send(MOVE)
                    # handle human player
                    if players[player].human:
                        players[player].send(INPUT, input())
                moves = [(process.nr, process.get(MOVE), process.name) for process in players
                         if process.nr in active_players]
                do_moves(game, moves)
                if game.free_card_player:
                    handle_free_card_from_dicard(game)
                if len(game.hand[0]) > 1:
                    rotate_hands(game)
                active_players = [player for player in range(n_players) if game.hand[player]]
            game.end_age(age, [process.name for process in players])

        send_to_all(END_GAME)
        return game.end_game()                

    results = {process.name: 0 for process in players}
    timeouts = 0
    table_permutation = permutations(range(n_players))
    next(table_permutation)
    for game_nr in range(n_games):
        try:
            wonders = sample(WONDERS, n_players)
            print(f'game nr {game_nr}')
            for nr in range(n_players):
                print(f'{players[nr].name}: {wonders[nr]}')
            game = SevenWonders(n_players, wonders, verbose)
            game_winners = play_game(game)
            if verbose:
                for process in players:
                    print((f'player {process.name} got '
                        f'{game.points[process.nr]} points'))
        except DeadPlayer as dead_player:
            dead = dead_player.nr
            print(f'player {dead} not responding...')
            # game_winners = [player for player in range(n_players)
            #                 if player != dead]
            game_winners = []
            timeouts += 1
            for process in players:
                process.restart()
        winners = [process.name
                   for process in players
                   if process.nr in game_winners]
        print(f'winners: {winners}')
        for process in players:
            if process.nr in game_winners:
                results[process.name] += 1
        print(f'\nwins so far: {results}')
        print(f'timeouts: {timeouts}\n')

        new_permutation = next(table_permutation)
        players = sorted(players, key=lambda process: process.original_nr)
        for player in range(n_players):
            players[player].nr = new_permutation[player]
        players = sorted(players, key=lambda process: process.nr)

    for process in players:
        process.kill()

    return results


def start_player(player_class: AbstractPlayer, nr: int,
                 conn: Connection, prepare_time: float,
                 move_time: float, n_players: int) -> None:
    player = player_class(nr, conn, prepare_time, move_time, n_players)
    player.play()