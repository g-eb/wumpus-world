from .square_type import SquareType


class Player(SquareType):
    def __init__(self):
        super().__init__(True)
        self.hasGold = False
        # self.headingDirection = Direction.DOWN

    def getConsoleGraphic(self):
        return 'P'
