from typing import Optional, Type
from abc import ABC, abstractmethod


class SquareType(ABC):
    color = "#000000"
    is_dangerous = False

    @staticmethod
    def get_effect() -> Optional[Type["SquareType"]]:
        return None

    @abstractmethod
    def __init__(self) -> None:
        pass
