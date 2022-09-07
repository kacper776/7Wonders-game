from random import choice

from game import *
from cards import CARDS
from players.base_player import AbstractPlayer
import brazilian_strategy


class BrazilianPlayer(AbstractPlayer):
    def prepare(self) -> None:
        self.rules = {}
        for card in [c for c in CARDS if max(c.copies) < 5]:
            self.rules[card.name] = getattr(brazilian_strategy, card.name)
    
    def move_score(self, move: Move):
        return self.rules[move.card.name](self.game, self.nr)

    def choose_move(self, moves: "list[Move]") -> Move:
        wonder_moves = [move for move in moves if move.type == 'build_wonder']
        play_moves = wonder_moves = [move for move in moves if move.type == 'play']
        sell_moves = [move for move in moves if move.type == 'sell']
        if wonder_moves:
            return choice(wonder_moves)
        if play_moves:
            best_move = max(moves, key=lambda move: self.move_score(move))
            if self.move_score(best_move) > 0:
                return best_move
        return choice(sell_moves)
       