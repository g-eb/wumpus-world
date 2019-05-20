from wumpus_world.game.squares.no_dragon import NoDragon
from wumpus_world.game.squares.no_hole import NoHole
from wumpus_world.game.squares.safe import Safe


class KnowledgeSquare:
    MAX_ONE_FIELD_ELEMENTS = 5
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.knowledge = []
        self.visited = False
        self.solved = False

    def setAsVisited(self):
        self.visited = True

    def setAsSolved(self):
        self.solved = True

    def addKnowledge(self, new):
        self.knowledge.append(new)

    def setAsSafe(self):
        if self.solved:
            return
        self.knowledge.append(Safe())
        self.solved = True

    def assumeSafty(self):
        classes = []
        for know in self.knowledge:
            classes.append(know.__class__)
        if classes.__contains__(NoDragon().__class__) and classes.__contains__(NoHole().__class__):
            self.setAsSafe()

    def isSafe(self):
        for know in self.knowledge:
            if know.__class__ == Safe().__class__:
                return True
        return False

    def getTextRepresentation(self):
        graphic = "|"
        uniqueElements = self.__getUniqueKnowledge()
        for empty in range(self.MAX_ONE_FIELD_ELEMENTS - len(uniqueElements)):
            graphic += " "
        for el in uniqueElements:
            graphic += el.text
        graphic += "|"
        return graphic

    def __getUniqueKnowledge(self):
        uniqueElements = []
        for know in self.knowledge:
            unique = True
            for e in uniqueElements:
                if e.__class__ == know.__class__:
                    unique = False
                    break
            if unique:
                uniqueElements.append(know)
        return uniqueElements
