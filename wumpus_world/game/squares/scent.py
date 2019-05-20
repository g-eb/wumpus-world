from .square_type import SquareType


class Scent(SquareType):
    color = "#b55903"
    text = "~"

    def __init__(self):
        super().__init__(False)

    def getCause(self):
        from wumpus_world.game.squares.dragon import Dragon
        return Dragon()
