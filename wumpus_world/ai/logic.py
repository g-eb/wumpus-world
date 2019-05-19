from enum import Enum
from abc import ABC


class Operator(Enum):
    AND = 'and'
    OR = 'or'

    def __repr__(self):
        return " {} ".format(self.value)


class Fact(ABC):
    def __init__(self, x, y, negated=False):
        self.x = x
        self.y = y
        self.negated = negated

    def __repr__(self):
        negation = '~' if self.negated else ''
        cls = self.__class__.__name__

        return "{}{}({}, {})".format(negation, cls, self.x, self.y)

    def __invert__(self):
        return type(self)(self.x, self.y, negated=not self.negated)

    def __and__(self, other):
        return Sentence([self, Operator.AND, other])

    def __or__(self, other):
        return Sentence([self, Operator.OR, other])

    def implicate(self, neighbors):
        pass


class Sentence(object):
    def __init__(self, components=()):
        self.components = list(components)

    def __repr__(self, nested=False):
        return "({})".format(
            ''.join([component.__repr__() for component in self.components])
        )

    def __and__(self, other):
        return Sentence([self, Operator.AND, other])

    def __or__(self, other):
        return Sentence([self, Operator.OR, other])


class Empty(Fact):
    def implicate(self, neighbors):
        components = []

        for neighbor in neighbors:
            components.append(Ok(neighbor.x, neighbor.y))
            components.append(Operator.AND)

        return Sentence(components)


class Ok(Fact):
    pass


class Wind(Fact):
    def implicate(self, neighbors):
        components = []

        for neighbor in neighbors:
            components.append(Hole(neighbor.x, neighbor.y))
            components.append(Operator.OR)

        return Sentence(components)


class Hole(Fact):
    pass


class Scent(Fact):
    def implicate(self, neighbors):
        components = []

        for neighbor in neighbors:
            components.append(Dragon(neighbor.x, neighbor.y))
            components.append(Operator.OR)

        return Sentence(components)


class Dragon(Fact):
    pass


class Shine(Fact):
    def implicate(self, neighbors):
        components = []

        for neighbor in neighbors:
            components.append(Gold(neighbor.x, neighbor.y))
            components.append(Operator.OR)

        return Sentence(components)


class Gold(Fact):
    pass
