from wumpus_world.game.squares.dragon import Dragon
from wumpus_world.game.squares.hole import Hole
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

    def addKnowledge(self, x, y, newKnowledgeList : [SquareType]):
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
        for row in self.height:
            for col in self.width:
                self.knowledgeSquares[row][col].assumeSafty()

    def __isXYLegal(self, x, y):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return True
        else:
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
