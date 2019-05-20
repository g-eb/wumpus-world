from typing import Type

from .square_type import SquareType
from .scent import Scent


class Dragon(SquareType):
    color = "#aaf409"
    is_dangerous = True

    @staticmethod
    def get_effect() -> Type[Scent]:
        return Scent
