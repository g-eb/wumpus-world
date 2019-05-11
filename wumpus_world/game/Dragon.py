from wumpus_world.game.FieldType import FieldType
from wumpus_world.game.Scent import Scent

class Dragon(FieldType):
    def __init__(self):
        super().__init__(True)

    def getConsoleGraphic(self):
        return 'D'

    def getEffect(self):
        return Scent()
