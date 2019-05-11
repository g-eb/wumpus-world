from wumpus_world.game.FieldType import FieldType
from wumpus_world.game.Direction import Direction
class Player(FieldType):
    def __init__(self):
        super().__init__(True)
        self.hasGold = False
        #self.headingDirection = Direction.DOWN

    def getConsoleGraphic(self):
        return 'P'
