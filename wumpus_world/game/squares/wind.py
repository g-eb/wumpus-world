from .square_type import SquareType


class Wind(SquareType):
    color = "#acb7b6"
    text = "="

    def __init__(self):
        super().__init__(False)

    def getCause(self):
        from wumpus_world.game.squares.hole import Hole
        return Hole()
