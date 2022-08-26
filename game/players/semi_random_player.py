from random import choice

from players.base_player import AbstractPlayer


class SemiRandomPlayer(AbstractPlayer):
    def prepare(self) -> None:
        pass
    
    def choose_move(self, moves: "tuple[tuple]") -> tuple:
        non_sell_moves = [move for move in moves if move[0] != 'sell']
        if non_sell_moves:
            return choice(non_sell_moves)
        move = choice(moves)
        return move

    