from wumpus_world.game.FieldType import FieldType

class Scent(FieldType):
    def __init__(self):
        super().__init__(False)

    def getConsoleGraphic(self):
        return '~'
