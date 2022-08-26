from multiprocessing.connection import Connection
from abc import ABC, abstractmethod
from resource import getrusage, RUSAGE_SELF

from game.game import *


class AbstractPlayer(ABC):
    def __init__(self, nr: int, conn: Connection,
                 prepare_time: float, move_time: float):
        self.nr = nr
        self.game = None
        self.conn = conn
        self.prepare_time = prepare_time
        self.move_time = move_time

    def suicide(self) -> None:
        self.conn.close()
        exit(0)

    def send(self, message_type: str, message=None) -> None:
        self.conn.send((message_type, message))
    
    def get(self, message_type: str):
        type_got, data = self.conn.recv()
        if type_got == END_GAME:
            self.play()
        assert(type_got == message_type)
        return data

    def limited_time(self, function: Callable, time_limit: float):
        start_time = getrusage(RUSAGE_SELF).ru_utime
        function()
        end_time = getrusage(RUSAGE_SELF).ru_utime
        if end_time - start_time > time_limit:
            self.suicide()

    @abstractmethod
    def prepare(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def choose_move(self, moves: "tuple[tuple]") -> tuple:
        raise NotImplementedError

    def play(self):
        self.game = self.get(DATA)
        self.limited_time(self.prepare, self.prepare_time)
        self.send(READY)
        while True:
            self.game = self.get(DATA)
            self.get(MOVE)
            move = self.choose_move(self.game.moves(self.nr))
            self.send(MOVE, move)

