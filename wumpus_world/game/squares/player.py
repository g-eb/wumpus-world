from .square_type import SquareType


class Player(SquareType):
    color = "#f9c8a9"
    text = "P"

    def __init__(self):
        super().__init__(False)
        self.hasGold = False
