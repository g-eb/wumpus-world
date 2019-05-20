from typing import List, Type

from .squares.square_type import SquareType


class Square:
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
        return len(self._elements)

    @property
    def sorted_elements(self) -> List[Type[SquareType]]:
        return sorted(self._elements, key=lambda element: element.__name__)

    def visit(self) -> None:
        if not self._visited:
            self._visited = True

    def is_occupied(self) -> bool:
        for element in self._elements:
            if element.is_dangerous:
                return True

        return False

    def has(self, typename: Type[SquareType]) -> bool:
        for element in self._elements:
            if element == typename:
                return True

        return False

    def has_dangerous_element(self) -> bool:
        for element in self._elements:
            if element.is_dangerous:
                return True

        return False

    def add_type(self, typename: Type[SquareType]) -> None:
        self._elements.append(typename)

    def remove_type(self, typename: Type[SquareType]) -> None:
        removed = False
        elements = []

        for element in self._elements:
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
