from random import randint
from random import shuffle
from .direction import Direction
from .square import Square
from .squares.player import Player
from .squares.dragon import Dragon
from .squares.hole import Hole
from .squares.gold import Gold


class Map:
    dragonsOccurrenceFrequency = 0.1    # (1,0)
    holesOccurrenceFrequency = 0.1      # (1,0)

    def __init__(self, width, height):
        self.playerPosX = 0
        self.playerPosY = 0
        self.width = width
        self.height = height
        self.gameOver = False
        self.squares = [
            [Square(j, i) for j in range(width)] for i in range(height)
        ]
        self.__randomMap()

    def move(self, direction):
        if self.gameOver:
            return
        if direction == Direction.DOWN.value:
            self.__tryMove(self.playerPosX, self.playerPosY + 1)
        elif direction == Direction.UP.value:
            self.__tryMove(self.playerPosX, self.playerPosY - 1)
        elif direction == Direction.LEFT.value:
            self.__tryMove(self.playerPosX - 1, self.playerPosY)
        elif direction == Direction.RIGHT.value:
            self.__tryMove(self.playerPosX + 1, self.playerPosY)

    def __isXYLegal(self, x, y):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return True
        else:
            return False

    def __addAroundSquareEffect(self, x, y, effectType):
        if self.__isXYLegal(x - 1, y):
            self.squares[y][x - 1].addType(effectType)
        if self.__isXYLegal(x + 1, y):
            self.squares[y][x + 1].addType(effectType)
        if self.__isXYLegal(x, y - 1):
            self.squares[y - 1][x].addType(effectType)
        if self.__isXYLegal(x, y + 1):
            self.squares[y + 1][x].addType(effectType)

    def __removeAroundSquareEffect(self, x, y, effectTypeClass):
        if self.__isXYLegal(x - 1, y):
            self.squares[y][x - 1].removeType(effectTypeClass)
        if self.__isXYLegal(x + 1, y):
            self.squares[y][x + 1].removeType(effectTypeClass)
        if self.__isXYLegal(x, y - 1):
            self.squares[y - 1][x].removeType(effectTypeClass)
        if self.__isXYLegal(x, y + 1):
            self.squares[y + 1][x].removeType(effectTypeClass)

    def __addNewTypeToSquare(self, x, y, type):
        if not(self.__isXYLegal(x, y)):
            print("illegal square was given")
            return
        self.squares[y][x].addType(type)
        effect = type.getEffect()
        if (effect is not None):
            self.__addAroundSquareEffect(x, y, effect)

    def __randomMap(self):
        # put player on (0,0)
        self.squares[0][0].addType(Player())
        # rand dragons
        dragonsNum = randint(
            1,
            int(self.height * self.width * self.dragonsOccurrenceFrequency)
        )
        self.__addTypeToRandomSquares(Dragon(), dragonsNum)
        # rand holes
        holesNum = randint(
            1,
            int(self.height * self.width * self.holesOccurrenceFrequency)
        )
        self.__addTypeToRandomSquares(Hole(), holesNum)
        # rand gold
        self.__addTypeToRandomSquares(Gold(), 1)

    def __tryMove(self, x, y):
        if not(self.__isXYLegal(x, y)):
            return
        # make move
        player = self.squares[self.playerPosY][self.playerPosX].removeType(
            Player().__class__
        )
        if self.squares[y][x].hasDangerousElement():     # collison
            print("Game Over")
            self.gameOver = True
            return
        # add player to new square
        self.squares[y][x].addType(player)
        self.playerPosX = x
        self.playerPosY = y
        # check if the gold is there
        gold = self.squares[y][x].tryPickUpGold()
        if gold is not None:
            player.hasGold = True
            # delete shine
            self.__removeAroundSquareEffect(x, y, gold.getEffect().__class__)
        # check game end condition
        if y == 0 and x == 0 and player.hasGold:
            print("You've won!")
            print("Game Over")
            self.gameOver = True

    def __addTypeToRandomSquares(self, typeName, num):
        # get all not occupied squares
        emptyFields = []
        for row in range(self.height):
            for col in range(self.width):
                if not(self.squares[row][col].isOccupied()):
                    emptyFields.append((row, col))

        if num > emptyFields.__len__():
            print("Not enough space on the board")
            return
        # shuffle and take few(num) first empty squares
        shuffle(emptyFields)
        for el in range(num):
            self.__addNewTypeToSquare(emptyFields[el][1], emptyFields[el][0], typeName)
