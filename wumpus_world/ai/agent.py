from typing import cast, Dict, Optional, Set
from random import shuffle

from ..game.map import Map
from ..game.square import Square

import wumpus_world.ai.logic as logic
import wumpus_world.game.square_type as squares


class Agent(object):
    def __init__(self, map: Map) -> None:
        self._map = map
        self._neighbors_of_visited: Set[Square] = set()
        self._knowledge_base: Dict[str, Set[logic.Term]] = {
            "facts": set(),
            "clauses": set()
        }

        self.update_visited()
        self.learn_player_square()

    @property
    def facts(self) -> Set[logic.Fact]:
        return cast(Set[logic.Fact], self._knowledge_base["facts"])

    @property
    def clauses(self) -> Set[logic.Clause]:
        return cast(Set[logic.Clause], self._knowledge_base["clauses"])

    def knows(self, term: logic.Term) -> bool:
        if isinstance(term, logic.Fact):
            return term in self.facts

        return term in self.clauses

    def find_move(self) -> Optional[Square]:
        if len(self._neighbors_of_visited) == 0:
            return None

        if self._map.gold_picked:
            return self._map.at(0, 0)

        possible_squares = sorted(
            self._neighbors_of_visited, key=lambda square: Square.distance(
                square, self._map.at(*self._map.player_position)))

        for square in possible_squares:
            if self.prove(logic.Gold(square.x, square.y)):
                print("Found gold at {}!".format(square))

                return square

            if (self.prove(~logic.Hole(square.x, square.y)) and
                    self.prove(~logic.Dragon(square.x, square.y))):
                print("Found ok {}!".format(square))

                return square

        shuffle(possible_squares)

        square = possible_squares.pop()

        print('No ok squares, randomly picked {}!'.format(square))

        return square

    def learn(self, term: logic.Term) -> None:
        if isinstance(term, logic.Fact):
            neighbors = self._map.get_neighbors(term.x, term.y)

            self.facts.add(term)

            for new_term in term.implicate(neighbors):
                if not self.knows(new_term):
                    self.learn(new_term)

        if isinstance(term, logic.Clause):
            self.clauses.add(term)

    def learn_player_square(self) -> None:
        square = self._map.at(self._map.player_x, self._map.player_y)
        converter = {
            squares.Wind: logic.Wind,
            squares.Scent: logic.Scent,
            squares.Shine: logic.Shine
        }

        for square_type, logic_type in converter.items():
            if square.has(square_type):
                self.learn(logic_type(square.x, square.y))
            else:
                self.learn(~logic_type(square.x, square.y))

    def prove(self, conjecture: logic.Fact) -> bool:
        if self.knows(conjecture):
            return True

        negated_conjecture = ~conjecture

        if self.knows(negated_conjecture):
            return False

        for clause in [clause for
                       clause in self.clauses
                       if clause.has_atom(conjecture)]:
            proven = True
            entailment: logic.Term = cast(
                logic.Term, clause.entail(negated_conjecture))

            self.clauses.discard(clause)

            for atom in entailment.atomize():
                if not self.prove(~atom):
                    proven = False
                    break

            self.clauses.add(clause)

            if proven:
                # self.learn(conjecture)

                return True

        return False

    def update_visited(self) -> None:
        self._neighbors_of_visited.discard(
            self._map.at(*self._map.player_position))
        self._neighbors_of_visited.update(
            [square for square
             in self._map.get_neighbors(*self._map.player_position)
             if not square.visited])
