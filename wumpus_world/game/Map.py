from random import randint
from wumpus_world.game.Field import Field
from wumpus_world.game.Player import Player
from wumpus_world.game.Dragon import Dragon
from wumpus_world.game.Hole import Hole
from wumpus_world.game.Gold import Gold
from wumpus_world.game.Direction import Direction


class Map:
    dragonsOccurrenceFrequency = 0.1    # (1,0)
    holesOccurrenceFrequency = 0.1      # (1,0)

    def __init__(self, width, height):
        self.playerPosX = 0
        self.playerPosY = 0
        self.width = width
        self.height = height
        self.gameOver = False
        self.fields = [[Field() for j in range(width)] for i in range(height)]

    def __isXYLegal(self, x, y):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return True
        else:
            return False

    def __addAroundFieldEffect(self, x, y, effectType):
        if self.__isXYLegal(x-1, y):
            self.fields[y][x-1].addType(effectType)
        if self.__isXYLegal(x+1, y):
            self.fields[y][x+1].addType(effectType)
        if self.__isXYLegal(x, y-1):
            self.fields[y-1][x].addType(effectType)
        if self.__isXYLegal(x, y+1):
            self.fields[y+1][x].addType(effectType)

    def addNewTypeToField(self, x, y, type):
        if not(self.__isXYLegal(x, y)):
            print("illegal field was given")
            return
        self.fields[y][x].addType(type)
        effect = type.getEffect()
        if (effect is not None):
            self.__addAroundFieldEffect(x, y, effect)

    def randomMap(self):
        # put player on (0,0)
        self.fields[0][0].addType(Player())
        # rand dragons
        dragonsNum = randint(1, self.height*self.width*self.dragonsOccurrenceFrequency)
        self.__addTypeToRandomFields(Dragon(), dragonsNum)
        # rand holes
        holesNum = randint(1, self.height*self.width*self.holesOccurrenceFrequency)
        self.__addTypeToRandomFields(Hole(), holesNum)
        # rand gold
        self.__addTypeToRandomFields(Gold(), 1)

    def printStatus(self):
        for row in range(self.height):
            for col in range(self.width):
                print(self.fields[row][col].getGraphic(), end="")
            print()

    def __action(self):
        self.printStatus()
        direction = input()
        if direction == Direction.DOWN.value:
            self.__tryMove(self.playerPosX, self.playerPosY+1)
        elif direction == Direction.UP.value:
            self.__tryMove(self.playerPosX, self.playerPosY-1)
        elif direction == Direction.LEFT.value:
            self.__tryMove(self.playerPosX-1, self.playerPosY)
        elif direction == Direction.RIGHT.value:
            self.__tryMove(self.playerPosX+1, self.playerPosY)

    def __tryMove(self, x, y):
        if not(self.__isXYLegal(x, y)):
            return
        # make move
        player = self.fields[self.playerPosY][self.playerPosX].removeType(Player().__class__)
        if self.fields[y][x].hasDangerousElement():     #collison
            self.printStatus()
            print("Game Over")
            self.gameOver = True
            return
        # add player to new field
        self.fields[y][x].addType(player)
        self.playerPosX = x
        self.playerPosY = y
        # check if the gold is there
        if self.fields[y][x].tryPickUpGold():
            player.hasGold = True
        # check game end condition
        if y == 0 and x == 0 and player.hasGold == True:
            self.printStatus()
            print("You've won!")
            print("Game Over")
            self.gameOver = True

    def startGame(self):
        while not(self.gameOver):
            self.__action()

    def __addTypeToRandomFields(self, typeName, num):
        for el in range(num):
            wasSet = False
            while not(wasSet):
                x = randint(0, self.width - 1)
                y = randint(0, self.height - 1)
                if not(self.fields[y][x].isOccupied()):
                    self.addNewTypeToField(x, y, typeName)
                    wasSet = True

