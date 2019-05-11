from wumpus_world.game.FieldType import FieldType

class Shine(FieldType):
    def __init__(self):
        super().__init__(False)

    def getConsoleGraphic(self):
        return '*'
