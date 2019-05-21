from ..game.map import Map
from  .knowledgeMap import KnowledgeMap
from ..game.direction import Direction


class Agent:
    def __init__(self, map : Map):
        self.worldMap = map
        self.knowledgeMap = KnowledgeMap(map.width, map.height)
        self.__addNewFacts()
        self.previousSteps = [(map.playerPosX, map.playerPosY)]
        self.stepNum = 0
        self.reverseSteps = False
        self.knowledgeMap.printKnowledge()
        self.hasGold = False

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
        self.knowledgeMap.conclude()

    def makeMove(self):
        if self.worldMap.gameOver:
            return
        x = self.worldMap.playerPosX
        y = self.worldMap.playerPosY
        newX = self.worldMap.playerPosX
        newY = self.worldMap.playerPosY

        # go back if has gold
        if self.hasGold:
            self.goBack()
            self.knowledgeMap.printKnowledge()
            return

        # move
        safeAround = self.knowledgeMap.getSafeAround(x, y)
        saveNotVisited = self.knowledgeMap.getNonVisited(safeAround)
        # close safe unvisited
        if saveNotVisited.__len__() > 0:
            newX = saveNotVisited[0].x
            newY = saveNotVisited[0].y
            # prefer square with gold
            for sq in saveNotVisited:
                if sq.hasGold():
                    newX = sq.x
                    newY = sq.y
                    self.hasGold = True

            self.worldMap.move(self.getDirection(newX, newY))
            # add move to previous moves
            self.previousSteps.append((newX, newY))
            self.stepNum += 1
            self.reverseSteps = False
        else:
            # go back until safe unvisited is in range
            self.goBack()


        # add new facts
        self.__addNewFacts()
        self.knowledgeMap.printKnowledge()

    def goBack(self):
        if self.stepNum == 0:
            self.reverseSteps = True
        if self.reverseSteps:
            self.stepNum += 1
        else:
            self.stepNum -= 1
        if self.stepNum <0 or self.stepNum > self.previousSteps.__len__():
            return
        prevStep = self.previousSteps[self.stepNum]
        # dir = self.getDirection(prevStep[0], prevStep[1])
        # if dir is None:
        #     prevStep = self.previousSteps.pop()
        #     dir = self.getDirection(prevStep[0], prevStep[1])
        self.worldMap.move(self.getDirection(prevStep[0], prevStep[1]))

    def getDirection(self, newX, newY):
        currentX = self.worldMap.playerPosX
        currentY = self.worldMap.playerPosY
        if newX-currentX > 0:
            return Direction.RIGHT.value
        if newX-currentX < 0:
            return Direction.LEFT.value
        if newY-currentY > 0:
            return Direction.DOWN.value
        if newY-currentY < 0:
            return Direction.UP.value
        return None
