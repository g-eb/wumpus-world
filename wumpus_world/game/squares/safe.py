from .square_type import SquareType

class Safe(SquareType):
    color = "#fdd510"

    def __init__(self):
        super().__init__(False)
