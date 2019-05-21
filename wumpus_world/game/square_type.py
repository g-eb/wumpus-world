from typing import Optional, Type
from abc import ABC, abstractmethod


class SquareType(ABC):
    color = "#000000"
    is_dangerous = False

    @staticmethod
    def get_effect() -> Optional[Type['SquareType']]:
        return None

    @abstractmethod
    def __init__(self) -> None:
        pass


class Player(SquareType):
    color = "#f9c8a9"


class Wind(SquareType):
    color = "#acb7b6"


class Scent(SquareType):
    color = "#b55903"


class Shine(SquareType):
    color = "#fff693"


class Hole(SquareType):
    color = "#c9fffa"
    is_dangerous = True

    @staticmethod
    def get_effect() -> Type[Wind]:
        return Wind


class Dragon(SquareType):
    color = "#aaf409"
    is_dangerous = True

    @staticmethod
    def get_effect() -> Type[Scent]:
        return Scent


class Gold(SquareType):
    color = "#fcc510"

    @staticmethod
    def get_effect() -> Type[Shine]:
        return Shine
