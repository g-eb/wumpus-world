from typing import Type

from .square_type import SquareType
from .wind import Wind


class Hole(SquareType):
    color = "#c9fffa"
    is_dangerous = True

    @staticmethod
    def get_effect() -> Type[Wind]:
        return Wind
