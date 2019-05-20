from .squares.gold import Gold
from .squares.player import Player


class Square:
    def __init__(self, x, y):
        self.contains = []
        self.x = x
        self.y = y

    def addType(self, newType):
        self.contains.append(newType)

    def isOccupied(self):
        for t in self.contains:
            if t.isDangerous:
                return True
        return False

    # console printing is a little bit broken, because there can be multiple
    # same objects at the square
    def getGraphic(self):
        graphic = "|"
        for empty in range(self.MAX_ELEMENTS_NUM - len(self.contains)):
            graphic += " "
        for el in self.contains:
            graphic += el.getConsoleGraphic()
        graphic += "|"
        return graphic

    def removeType(self, typeClass):
        obj = self.getType(typeClass)
        if obj is not None:
            self.contains.remove(obj)
        return obj

    def getType(self, typeClass):
        obj = None
        for el in self.contains:
            if typeClass == el.__class__:
                obj = el
                break
        return obj

    def hasDangerousElement(self):
        for el in self.contains:
            if el.isDangerous:
                return True
        return False

    def tryPickUpGold(self):
        gold = None
        for el in self.contains:
            if el.__class__ == Gold().__class__:
                for el2 in self.contains:
                    if el2.__class__ == Player().__class__:
                        gold = el
                        break
                if gold is not None:
                    break
        if gold is not None:
            self.contains.remove(gold)
        return gold

    # badly written, change after all
    def getSquareEffects(self):
        list = []
        for el in self.contains:
            if el.__class__ != Player().__class__:
                list.append(el)
        return list

