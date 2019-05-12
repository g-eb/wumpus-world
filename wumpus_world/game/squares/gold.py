from .square_type import SquareType
from .shine import Shine


class Gold(SquareType):
    def __init__(self):
        super().__init__(False)

    def getConsoleGraphic(self):
        return 'g'

    def getEffect(self):
        return Shine()
