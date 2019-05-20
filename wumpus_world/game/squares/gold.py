from typing import Type

from .square_type import SquareType
from .shine import Shine


class Gold(SquareType):
    color = "#fcc510"

    @staticmethod
    def get_effect() -> Type[Shine]:
        return Shine
