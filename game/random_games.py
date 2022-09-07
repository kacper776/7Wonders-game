from random import choice

from game import *
from heuristics import fill_unknown_information

def random_game(game: SevenWonders, first_move: Move, nr: int,
                hands_seen: "list[list[Move]]",
                discard_seen: "list[Move]") -> "tuple[bool][list[Move]]":
        n_players = len(game.board)
        def rotate_hands(game: SevenWonders) -> None:
            dir = [-1, 1, -1][game.age - 1]
            saved_hand = [copy(game.hand[player])
                          for player in range(n_players)]
            for player in range(n_players):
                game.hand[player] = saved_hand[(player - dir + n_players)\
                                                % n_players]
        
        def semi_random_move(moves: "list[Move]") -> tuple:
            non_sell_moves = [move for move in moves if move.type != 'sell']
            if non_sell_moves:
                return choice(non_sell_moves)
            return choice(moves)

        game = game.copy()
        curr_age = game.age
        moves_done = []
        first_move_done = False

        fill_unknown_information(game, nr, hands_seen,
                                 discard_seen)
        
        for age in range(curr_age, 4):
            if age != curr_age:
                game.start_age(age)
            active_players = [player for player in range(n_players)
                              if game.hand[player]]   
            while active_players:
                for player in active_players:
                    moves = game.moves(player) #######
                    if not moves: #########
                        print(player, game.hand[player])
                    move = semi_random_move(moves)
                    if not first_move_done and player == nr:
                        move = first_move
                        first_move_done = True
                    if player == nr and age == curr_age:
                        moves_done.append(move)
                    game.do_move(player, move)
                game.resolve_actions()
                if game.free_card_player:
                    free_card_move = choice(game.moves(game.free_card_player))
                    game.do_move(game.free_card_player, free_card_move)
                    game.resolve_actions()
                if len(game.hand[nr]) > 1:
                    rotate_hands(game)
                active_players = [player for player in range(n_players)
                                  if game.hand[player]]
            game.end_age(age)

        return (nr in game.end_game(), moves_done)

    