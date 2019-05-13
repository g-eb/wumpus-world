from .square_type import SquareType


class Player(SquareType):
    color = "#efb794"

    def __init__(self):
        super().__init__(True)
        self.hasGold = False
