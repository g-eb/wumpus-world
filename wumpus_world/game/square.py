from typing import List, Type

from .square_type import SquareType, Player


class Square:
    @staticmethod
    def distance(square_1, square_2) -> int:
        return abs(square_1.x - square_2.x) + abs(square_1.y - square_2.y)

    def __init__(self, x: int, y: int) -> None:
        self._elements: List[Type[SquareType]] = []
        self._x = x
        self._y = y
        self._visited = False

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def visited(self) -> bool:
        return self._visited

    @property
    def size(self) -> int:
        return len(self.elements)

    @property
    def elements(self) -> List[Type[SquareType]]:
        return self._elements

    def __repr__(self) -> str:
        return "Square({}, {})".format(self.x, self.y)

    def visit(self) -> None:
        if not self._visited:
            self._visited = True

    def is_occupied(self) -> bool:
        for element in self.elements:
            if element.is_dangerous or element == Player:
                return True

        return False

    def has(self, typename: Type[SquareType]) -> bool:
        return typename in self.elements

    def has_dangerous_element(self) -> bool:
        for element in self.elements:
            if element.is_dangerous:
                return True

        return False

    def add_type(self, typename: Type[SquareType]) -> None:
        self.elements.append(typename)

    def remove_type(self, typename: Type[SquareType]) -> None:
        removed = False
        elements = []

        for element in self.elements:
            if element == typename:
                if removed:
                    # First element with a type typename was deleted.
                    # The rest elements of that type is copied to the new list.
                    elements.append(element)
                else:
                    removed = True
            else:
                elements.append(element)

        self._elements = elements
