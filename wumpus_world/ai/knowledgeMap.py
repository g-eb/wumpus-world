from wumpus_world.game.squares.dragon import Dragon
from wumpus_world.game.squares.hole import Hole
from wumpus_world.game.squares.gold import Gold
from wumpus_world.game.squares.no_dragon import NoDragon
from wumpus_world.game.squares.no_hole import NoHole
from .knowledgeSquare import KnowledgeSquare
from ..game.squares.square_type import SquareType

class KnowledgeMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.knowledgeSquares = [
            [KnowledgeSquare(j, i) for j in range(self.width)] for i in range(self.height)
        ]

    def addKnowledge(self, x, y, newKnowledgeList):
        causes = []
        for know in newKnowledgeList:
            if know.getCause() is not None:
                causes.append(know.getCause().__class__)
                self.knowledgeSquares[y][x].addKnowledge(know)
        around = self.getAroundSquares(x, y)
        if not(causes.__contains__(Dragon().__class__)):
            for sq in around:
                sq.addKnowledge(NoDragon())
        if not(causes.__contains__(Hole().__class__)):
            for sq in around:
                sq.addKnowledge(NoHole())

        #if field is dragon and hole free than it's safe
        for row in range(self.height):
            for col in range(self.width):
                self.knowledgeSquares[row][col].assumeSafty()

    def conclude(self):
        while True:
            knowledgeChanged = False
            for row in range(self.height):
                for col in range(self.width):
                    if self.knowledgeSquares[row][col].solved:
                        continue
                    info = self.knowledgeSquares[row][col].getAdditionalInformations()
                    for i in info:
                        around = self.getAroundSquares(col, row)
                        # if object tak can cause effect is near it can't be conclude that
                        # this object cause this effect or not
                        if self.containsClass(around, i.getCause().__class__):
                            continue
                        nonSafeAround = self.getNonSafe(around)
                        if i.getCause().__class__ == Gold().__class__:
                            nonSafeAround = self.getNonVisited(around)
                        nonImportant = self.getNonImportant(nonSafeAround)
                        if nonImportant.__len__() == 1:
                            knowledgeChanged = True
                            nonImportant[0].addKnowledge(i.getCause())
                            if info.__len__() == 1:
                                self.knowledgeSquares[row][col].setAsSolved()
                            # what if field contains solve and unsolved knowledge?
                            # sure there is a danger
                            # change facts
                        # check other possibilities
                        # partially solved??
            if not(knowledgeChanged):
                break

    def __isXYLegal(self, x, y):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return True
        else:
            return False

    def containsClass(self, squaresList, searchedClass):
        for sq in squaresList:
            if sq.containsClass(searchedClass):
                return True
        return False

    def getAroundSquares(self, x, y):
        aroundSquares = []
        if self.__isXYLegal(x - 1, y):
            aroundSquares.append(self.knowledgeSquares[y][x - 1])
        if self.__isXYLegal(x + 1, y):
            aroundSquares.append(self.knowledgeSquares[y][x + 1])
        if self.__isXYLegal(x, y - 1):
            aroundSquares.append(self.knowledgeSquares[y - 1][x])
        if self.__isXYLegal(x, y + 1):
            aroundSquares.append(self.knowledgeSquares[y + 1][x])
        return aroundSquares

    def getNonSafe(self, squaresList):
        unsafe = []
        for sq in squaresList:
            if not(sq.isSafe()):
                unsafe.append(sq)
        return unsafe

    def getSafe(self, squareList):
        safe = []
        for sq in squareList:
            if sq.isSafe():
                safe.append(sq)
        return safe

    def getAllSafeSquares(self):
        safe = []
        for row in range(self.height):
            for col in range(self.width):
                if self.knowledgeSquares[row][col].isSafe():
                    safe.append(self.knowledgeSquares[row][col])
        return safe

    def getNonVisited(self, squaresList):
        unvisited = []
        for sq in squaresList:
            if not(sq.visited):
                unvisited.append(sq)
        return unvisited

    def getNonImportant(self, squaresList):
        unimportant = []
        for sq in squaresList:
            if not(sq.isImportant()):
                unimportant.append(sq)
        return unimportant

    def printKnowledge(self):
        for col in range(self.width*(KnowledgeSquare.MAX_ONE_FIELD_ELEMENTS+3) + 2):
            print("-", end="")
        print()
        for row in range(self.height):
            print("|", end="")
            for col in range(self.width):
                print(self.knowledgeSquares[row][col].getTextRepresentation(), end="")
            print("|")

    def getSafeAround(self, x, y):
        around = self.getAroundSquares(x, y)
        safe = self.getSafe(around)
        return safe
