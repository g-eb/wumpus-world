from wumpus_world.game.squares.no_dragon import NoDragon
from wumpus_world.game.squares.no_hole import NoHole
from wumpus_world.game.squares.safe import Safe


class KnowledgeSquare:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.knowledge = []
        self.visited = False
        self.solved = False

    def setAsVisited(self):
        self.visited = True

    def setAsSolved(self):
        self.solved = True

    def addKnowledge(self, new):
        self.knowledge.append(new)

    def assumeSafty(self):
        classes = []
        for know in self.knowledge:
            classes.append(know.__class__)
        if classes.__contains__(NoDragon().__class__) and classes.__contains__(NoHole().__class__):
            self.knowledge.append(Safe())

    def isSafe(self):
        for know in self.knowledge:
            if know.__class__ == Safe().__class__:
                return True
        return False
