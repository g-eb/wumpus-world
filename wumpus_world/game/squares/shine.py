from .square_type import SquareType


class Shine(SquareType):
    color = "#fff693"

    def __init__(self):
        super().__init__(False)

    def getCause(self):
        from wumpus_world.game.squares.gold import Gold
        return Gold()
