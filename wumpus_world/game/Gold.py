from wumpus_world.game.FieldType import FieldType
from  wumpus_world.game.Shine import Shine

class Gold(FieldType):
    def __init__(self):
        super().__init__(False)

    def getConsoleGraphic(self):
        return 'g'

    def getEffect(self):
        return Shine()
