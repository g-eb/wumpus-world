from .square_type import SquareType


class Player(SquareType):
    color = "#f9c8a9"

    def __init__(self):
        super().__init__(True)
        self.hasGold = False
