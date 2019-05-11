from wumpus_world.game.FieldType import FieldType
from wumpus_world.game.Wind import Wind

class Hole(FieldType):
    def __init__(self):
        super().__init__(True)

    def getConsoleGraphic(self):
        return 'H'

    def getEffect(self):
        return Wind()
