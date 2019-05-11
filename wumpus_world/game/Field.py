from wumpus_world.game.FieldType import FieldType

class Field:
    MAX_ELEMENTS_NUM = 3
    def __init__(self):
        self.contains = []

    def addType(self, newType):
        self.contains.append(newType)

    def isOccupied(self):
        for t in self.contains:
            if t.isDangerous == True:
                return True
        return False

    # console printing is a little bit broken, because there can be multiple same objects on the field
    def getGraphic(self):
        graphic = "|"
        for empty in range(self.MAX_ELEMENTS_NUM - len(self.contains)):
            graphic += " "
        for el in self.contains:
            graphic += el.getConsoleGraphic()
        graphic += "|"
        return graphic
