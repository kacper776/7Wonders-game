from copy import copy
from random import sample
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection

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
        self.human = human
        self.parent_conn, child_conn = Pipe()
        self.process = Process(target=function,
                               args=(player_class, nr, child_conn,
                                     prepare_time, move_time, n_players),
                               name=name,
                               daemon=True)
        self.process.start()
        
    def send(self, message_type, message=None) -> None:
        self.parent_conn.send((message_type, message))

    def get(self, message_type):
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

    # TODO: cover discard
    def update_players_data(game: SevenWonders, active_players: "list[int]") -> None:
        saved_hand = [copy(game.hand[player]) for player in range(n_players)]
        for player, process in enumerate(players):
            if player not in active_players:
                continue
            other_players = [p for p in range(n_players) if p != player]
            for other_player in other_players:
                game.hand[other_player] = None
            process.send(DATA, game)
            for other_player in other_players:
                game.hand[other_player] = saved_hand[other_player]
            
    def do_moves(game: SevenWonders, moves: "list[tuple[int][Move]]") -> None:
        for player, move in moves:
            game.do_move(player, move)
        game.resolve_actions()

    def rotate_hands(game: SevenWonders, age: int) -> None:
        dir = [1, -1, 1][age - 1]
        saved_hand = [copy(game.hand[player]) for player in range(n_players)]
        for player in range(n_players):
            game.hand[player] = saved_hand[(player - dir + n_players) % n_players]

    def handle_free_card_from_dicard(game: SevenWonders) -> None:
        player = game.free_card_choice
        update_players_data(game, [player])
        players[player].send(MOVE)
        move = players[player].get(MOVE)
        do_moves(game, [(player, move)])

    def play_game(game: SevenWonders) -> "list[int]":
        update_players_data(game, range(n_players))
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
                moves = [(process.nr, process.get(MOVE)) for process in players
                         if process.nr in active_players]
                do_moves(game, moves)
                if game.free_card_choice:
                    handle_free_card_from_dicard(game)
                if len(game.hand[0]) > 1:
                    rotate_hands(game, age)
                active_players = [player for player in range(n_players) if game.hand[player]]
            game.end_age(age)

        send_to_all(END_GAME)
        return game.end_game()                

    results = [0] * n_players
    for game_nr in range(n_games):
        try:
            wonders = sample(WONDERS, n_players)
            print(f'game nr {game_nr}\nwonders:\n', wonders, sep='')
            game = SevenWonders(n_players, wonders, verbose)
            game_winners = play_game(game)
        except DeadPlayer as dead_player:
            dead = dead_player.nr
            game_winners = [player for player in range(n_players)
                            if player != dead]
        print(f'winners: {game_winners}')
        for player in range(n_players):
            if player in game_winners:
                results[player] += 1

    for process in players:
        process.kill()

    return results


def start_player(player_class: AbstractPlayer, nr: int,
                 conn: Connection, prepare_time: float,
                 move_time: float, n_players: int) -> None:
    player = player_class(nr, conn, prepare_time, move_time, n_players)
    player.play()