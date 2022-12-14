from base import *
from players.base_player import AbstractPlayer


class HumanPlayer(AbstractPlayer):
    def prepare(self) -> None:
        pass

    def choose_move(self, moves: "list[Move]") -> Move:
        for nr, move in enumerate(moves):
            print(nr, move)
        move_nr = int(self.get(INPUT))
        return moves[move_nr]
