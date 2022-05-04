from game_field import GameField
from random import randint


class ArtificialIntelligence:
    @staticmethod
    def make_move(field: GameField):
        is_moved = False
        while not is_moved:
            x = randint(0, field.x - 1)
            y = randint(0, field.y - 1)
            if field.try_put(x, y):
                is_moved = True
