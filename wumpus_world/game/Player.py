from wumpus_world.game.FieldType import FieldType

class Player(FieldType):
    def __init__(self):
        super().__init__(True)

    def getConsoleGraphic(self):
        return 'P'
