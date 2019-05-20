from typing import List, Tuple, Type
from random import randint
from random import shuffle

from .direction import Direction
from .square import Square
from .squares.square_type import SquareType
from .squares.player import Player
from .squares.dragon import Dragon
from .squares.hole import Hole
from .squares.gold import Gold


class Map:
    _dragons_frequency = 0.1
    _holes_frequency = 0.1

    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._victory = False
        self._game_over = False
        self._player_x = 0
        self._player_y = 0
        self._player_has_gold = False
        self._squares = [
            [Square(j, i) for j in range(width)] for i in range(height)]

        self._generate_map()

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def game_over(self) -> bool:
        return self._game_over

    @property
    def victory(self) -> bool:
        return self._victory

    @property
    def loss(self) -> bool:
        return not self._victory

    @property
    def player_x(self) -> int:
        return self._player_x

    @property
    def player_y(self) -> int:
        return self._player_y

    @property
    def player_position(self) -> Tuple[int, int]:
        return (self._player_x, self._player_y)

    def at(self, x: int, y: int) -> Square:
        if self._are_valid_coordinates(x, y):
            return self._squares[y][x]

        raise IndexError("Map does not contain a square ({}, {})".format(x, y))

    def get_neighbors(self, x: int, y: int) -> List[Square]:
        neighbors = []

        if self._are_valid_coordinates(x - 1, y):
            neighbors.append(self.at(x - 1, y))
        if self._are_valid_coordinates(x + 1, y):
            neighbors.append(self.at(x + 1, y))
        if self._are_valid_coordinates(x, y - 1):
            neighbors.append(self.at(x, y - 1))
        if self._are_valid_coordinates(x, y + 1):
            neighbors.append(self.at(x, y + 1))

        return neighbors

    def move(self, direction: Direction) -> None:
        if self._game_over:
            return

        destination_x, destination_y = self._direction_to_point(direction)

        if self._are_valid_coordinates(destination_x, destination_y):
            destination = self.at(destination_x, destination_y)

            self.at(self._player_x, self._player_y).remove_type(Player)

            if destination.has_dangerous_element():
                self._game_over = True
                self._victory = False

                return

            destination.add_type(Player)
            destination.visit()
            self._player_x, self._player_y = destination_x, destination_y

            if destination.has(Gold):
                self._remove_type_from_square(
                    destination_x, destination_y, Gold)
                self._player_has_gold = True

            if (self._player_x == 0 and self._player_y == 0
                    and self._player_has_gold):
                self._game_over = True
                self._victory = True

    def _are_valid_coordinates(self, x: int, y: int) -> bool:
        return x >= 0 and x < self._width and y >= 0 and y < self._height

    def _direction_to_point(self, direction: Direction) -> Tuple[int, int]:
        return {
            Direction.UP: (self._player_x, self._player_y - 1),
            Direction.DOWN: (self._player_x, self._player_y + 1),
            Direction.LEFT: (self._player_x - 1, self._player_y),
            Direction.RIGHT: (self._player_x + 1, self._player_y)
        }[direction]

    def _generate_map(self):
        # Put the player at the square (0,0).
        self.at(0, 0).add_type(Player)

        # Generate dragons at random squares.
        dragons_number = randint(
            1,
            int(self._height * self._width * self._dragons_frequency)
        )
        self._add_type_to_random_squares(Dragon, dragons_number)

        # Generate holes at random squares.
        holes_number = randint(
            1,
            int(self._height * self._width * self._holes_frequency)
        )
        self._add_type_to_random_squares(Hole, holes_number)

        # Add gold at a random square.
        self._add_type_to_random_squares(Gold, 1)

    def _add_type_to_square(self, x: int, y: int,
                            typename: Type[SquareType]) -> None:
        effect = typename.get_effect()

        self.at(x, y).add_type(typename)

        if effect is not None:
            self._add_effect_to_neighbors(x, y, effect)

    def _remove_type_from_square(self, x: int, y: int,
                                 typename: Type[SquareType]) -> None:
        effect = typename.get_effect()

        self.at(x, y).remove_type(typename)

        if effect is not None:
            self._remove_effect_from_neighbors(x, y, effect)

    def _add_effect_to_neighbors(self, x: int, y: int,
                                 effect: Type[SquareType]) -> None:
        for square in self.get_neighbors(x, y):
            square.add_type(effect)

    def _remove_effect_from_neighbors(self, x: int, y: int,
                                      effect: Type[SquareType]) -> None:
        for square in self.get_neighbors(x, y):
            square.remove_type(effect)

    def _add_type_to_random_squares(self, typename: Type[SquareType],
                                    count: int) -> None:
        empty_squares_coordinates = []

        for y in range(self._height):
            for x in range(self._width):
                if not self.at(x, y).is_occupied():
                    empty_squares_coordinates.append((x, y))

        if count > len(empty_squares_coordinates):
            raise ValueError(
                "Not enough size to create {} object{} of class {}".format(
                    count, 's' if count != 1 else '', typename))

        shuffle(empty_squares_coordinates)

        for x, y in empty_squares_coordinates[:count]:
            self._add_type_to_square(x, y, typename)
