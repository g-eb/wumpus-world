from .game.map import Map
from .game.ui.window import Window
from .ai.agent import Agent


class App(object):
    _map_width = 12
    _map_height = 8
    _ai_timeout = 500

    def __init__(self) -> None:
        self._map = Map(self._map_width, self._map_height)
        self._agent = Agent(self._map)
        self._window = Window(self._map)

        self._set_key_bindings()

    def bind(self, key, handler) -> None:
        self._window.bind(key, handler)

    def start(self) -> None:
        self._window.after(self._ai_timeout, self.turn)
        self._window.show()

    def quit(self) -> None:
        self._window.close()

    def turn(self) -> None:
        destination_square = self._agent.find_move()

        if destination_square is not None and not self._map.game_over:
            self._map.move_at(destination_square.x, destination_square.y)

            if self._map.game_over:
                self._game_over()
            else:
                self._agent.update_visited()
                self._agent.learn_player_square()
                self._window.render()
                self._window.after(self._ai_timeout, self.turn)

    def _game_over(self):
        self._window.render()
        print("Game over, victory: {}".format(self._map.victory))

    def _set_key_bindings(self) -> None:
        self._window.bind("w", self.turn)
        self._window.bind("a", self.turn)
        self._window.bind("s", self.turn)
        self._window.bind("d", self.turn)
        self._window.bind("<Up>", self.turn)
        self._window.bind("<Left>", self.turn)
        self._window.bind("<Down>", self.turn)
        self._window.bind("<Right>", self.turn)
