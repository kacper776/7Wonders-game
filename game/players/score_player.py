from random import choice

from base import *
from heuristics import move_score, fill_unknown_information
from players.base_player import AbstractPlayer


class ScorePlayer(AbstractPlayer):
    def prepare(self) -> None:
        pass    

    def choose_move(self, moves: "list[Move]") -> Move:
        # for move in moves:
        #     if move.type == 'sell':
        #         continue
        #     print(move, end=' ')
        #     print(move_score(move, self.game, self.nr))
        # print()
        if self.game.free_card_choice == self.nr:
            return max(moves,
                       key=lambda move: move_score(move,
                                                   self.game,
                                                   self.nr))
        non_sell_moves = [move for move in moves if move.type != 'sell']
        sell_moves = [move for move in moves if move.type == 'sell']
        best_non_sell_move = max(non_sell_moves,
                                 key=lambda move: move_score(move,
                                                             self.game,
                                                             self.nr),
                                 default=None)
        if not sell_moves:
            return best_non_sell_move
        if not best_non_sell_move\
           or move_score(best_non_sell_move, self.game, self.nr) < 1.2:
            if sell_moves:
                return choice(sell_moves)
            return choice(moves)
        return best_non_sell_move
