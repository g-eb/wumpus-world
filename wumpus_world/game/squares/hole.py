from .square_type import SquareType
from .wind import Wind


class Hole(SquareType):
    def __init__(self):
        super().__init__(True)

    def getConsoleGraphic(self):
        return 'H'

    def getEffect(self):
        return Wind()
