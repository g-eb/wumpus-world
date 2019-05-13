from .square_type import SquareType
from .wind import Wind


class Hole(SquareType):
    color = "#303030"

    def __init__(self):
        super().__init__(True)

    def getEffect(self):
        return Wind()
