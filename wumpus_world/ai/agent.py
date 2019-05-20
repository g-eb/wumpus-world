from .knowledgeSquare import KnowledgeSquare
from ..game.map import Map
from  .knowledgeMap import KnowledgeMap
from ..game.squares.scent import Scent
from ..game.squares.wind import Wind
from ..game.squares.shine import Shine


class Agent:
    def __init__(self, map : Map):
        self.worldMap = map
        self.knowledgeMap = KnowledgeMap(map.width, map.height)
        #self.__addNewFacts()

    def __addNewFacts(self):
        x = self.worldMap.playerPosX
        y = self.worldMap.playerPosY
        if self.knowledgeMap.knowledgeSquares[y][x].visited:
            return
        self.knowledgeMap.knowledgeSquares[y][x].setAsVisited()

        # game over
        if self.worldMap.squares[y][x].hasDangerousElement():
            return
        self.knowledgeMap.knowledgeSquares[y][x].setAsSafe()
        self.knowledgeMap.addKnowledge(x, y, self.worldMap.squares[y][x].contains)



    def makeMove(self):
        if self.worldMap.gameOver:
            return
        # add new facts
        self.__addNewFacts()
        self.knowledgeMap.printKnowledge()
