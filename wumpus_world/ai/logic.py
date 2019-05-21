from typing import Any, List, Optional, Set
from abc import ABC, abstractmethod

from ..game.square import Square


class Term(ABC):
    @abstractmethod
    def atomize(self) -> Set['Fact']:
        pass

    def entail(self, other: 'Term') -> Optional['Term']:
        self_atoms = self.atomize()
        other_atoms = other.atomize()
        new_atoms = set()

        for self_atom in self_atoms:
            negated_atom = ~self_atom

            if negated_atom not in other_atoms:
                new_atoms.add(self_atom)

            other_atoms.discard(self_atom)
            other_atoms.discard(negated_atom)

        new_atoms |= other_atoms

        if len(new_atoms) == 0:
            return None

        if len(new_atoms) == 1:
            return new_atoms.pop()

        return Clause(*new_atoms)


class Fact(Term, ABC):
    def __init__(self, x: int, y: int, negated: bool = False) -> None:
        self.x = x
        self.y = y
        self.negated = negated

    def __repr__(self) -> str:
        negation = '~' if self.negated else ''
        cls = self.__class__.__name__

        return "{}{}({}, {})".format(negation, cls, self.x, self.y)

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __eq__(self, other: Any) -> bool:
        return (type(self) == type(other) and self.x == other.x
                and self.y == other.y and self.negated == other.negated)

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __invert__(self) -> 'Fact':
        return type(self)(self.x, self.y, negated=not self.negated)

    def atomize(self) -> Set['Fact']:
        return set([self])

    def implicate(self, neighbors: List[Square]) -> List[Term]:
        return []


class Clause(Term):
    def __init__(self, *facts) -> None:
        self._facts = set(facts)

    def __repr__(self) -> str:
        return " or ".join([str(fact) for fact in self._facts])

    def has_atom(self, fact: Fact) -> bool:
        return fact in self._facts

    def atomize(self) -> Set[Fact]:
        return set(self._facts)


class Wind(Fact):
    def implicate(self, neighbors: List[Square]) -> List[Term]:
        if self.negated:
            return [Clause(~self, ~Hole(neighbor.x, neighbor.y)) for neighbor
                    in neighbors]

        return [Clause(*[Hole(neighbor.x, neighbor.y) for neighbor
                         in neighbors])]


class Scent(Fact):
    def implicate(self, neighbors: List[Square]) -> List[Term]:
        if self.negated:
            return [Clause(~self, ~Dragon(neighbor.x, neighbor.y)) for neighbor
                    in neighbors]

        return [Clause(*[Dragon(neighbor.x, neighbor.y) for neighbor
                         in neighbors])]


class Shine(Fact):
    def implicate(self, neighbors: List[Square]) -> List[Term]:
        if self.negated:
            return [Clause(~self, ~Gold(neighbor.x, neighbor.y)) for neighbor
                    in neighbors]

        return [Clause(*[Gold(neighbor.x, neighbor.y) for neighbor
                         in neighbors])]


class Ok(Fact):
    pass


class Hole(Fact):
    pass


class Dragon(Fact):
    pass


class Gold(Fact):
    pass
