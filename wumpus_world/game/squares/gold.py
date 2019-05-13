from .square_type import SquareType
from .shine import Shine


class Gold(SquareType):
    color = "#eac312"

    def __init__(self):
        super().__init__(False)

    def getEffect(self):
        return Shine()
