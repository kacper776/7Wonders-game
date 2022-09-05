from multiprocessing.connection import Connection
from abc import ABC, abstractmethod
from resource import getrusage, RUSAGE_SELF
from copy import copy

from base import *
from game import *


class AbstractPlayer(ABC):
    def __init__(self, nr: int, conn: Connection,
                 prepare_time: float, move_time: float,
                 n_players: int) -> None:
        self.nr = nr
        self.game = None
        self.conn = conn
        self.prepare_time = prepare_time
        self.move_time = move_time
        self.n_players = n_players
        self.hands_seen = []
        self.discard_seen = []

    def suicide(self) -> None:
        self.conn.close()
        exit(0)

    def send(self, message_type: bytes, message: object=None) -> None:
        self.conn.send((message_type, message))
    
    def get(self, message_type: bytes) -> object:
        type_got, data = self.conn.recv()
        if type_got == END_GAME:
            self.hands_seen = []
            self.discard_seen = []
            self.play()
        assert(type_got == message_type)
        return data

    def limited_time(self, function: Callable, time_limit: float, args=()):
        start_time = getrusage(RUSAGE_SELF).ru_utime
        result = function(*args)
        end_time = getrusage(RUSAGE_SELF).ru_utime
        if end_time - start_time > time_limit:
            self.suicide()
        return result

    def remember_hand(self, hand: "list[Card]") -> None:
        if self.game.free_card_player == self.nr:
            self.discard_seen = hand
        else:
            if len(self.hands_seen) == 6:
                self.hands_seen = []
            self.hands_seen.append(hand)

    @abstractmethod
    def prepare(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def choose_move(self, moves: "list[Move]") -> Move:
        raise NotImplementedError

    def play(self) -> None:
        self.game, self.nr = self.get(DATA)
        self.limited_time(self.prepare, self.prepare_time)
        self.send(READY)
        while True:
            self.game, hand = self.get(DATA)
            self.get(MOVE)
            if self.game.free_card_player == self.nr:
                self.game.discard_pile = hand
            move = self.limited_time(self.choose_move,
                                     self.move_time,
                                     (self.game.moves(self.nr),))
            hand.remove(move.card)
            self.remember_hand(hand)
            self.send(MOVE, move)

