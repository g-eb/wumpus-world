from .square_type import SquareType

class Safe(SquareType):
    color = "#fdd510"
    text = "+"

    def __init__(self):
        super().__init__(False)
