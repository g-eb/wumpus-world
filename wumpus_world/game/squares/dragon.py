from .square_ype import SquareType
from .scent import Scent


class Dragon(SquareType):
    def __init__(self):
        super().__init__(True)

    def getConsoleGraphic(self):
        return 'D'

    def getEffect(self):
        return Scent()
