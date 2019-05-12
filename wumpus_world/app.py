from .game.map import Map
from .game.ui.window import Window


def run():
    map = Map(12, 8)
    window = Window(map)

    window.show()
