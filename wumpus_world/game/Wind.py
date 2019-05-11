from wumpus_world.game.FieldType import FieldType

class Wind(FieldType):
    def __init__(self):
        super().__init__(False)

    def getConsoleGraphic(self):
        return 'w'
