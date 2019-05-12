from .square_type import SquareType
from .scent import Scent


class Dragon(SquareType):
    color = "#074f09"
    symbol = '🔥'

    def __init__(self):
        super().__init__(True)

    def getEffect(self):
        return Scent()
