import random
from engine.input import Buttons


class MoveGame:
    def __init__(self, config):
        self.__grid_width = config.pair.grid_width
        self.__grid_height = config.pair.grid_height
        self.__state = {
            'y': 0,
            'x': 0
        }

    def update(self, players):
        x = self.__state.get('x', 0)
        y = self.__state.get('y', 0)

        player = players[0]
        direction = player.input.get_direction()
        if direction == Buttons.left:
            self.__state['x'] = (x - 1) % self.__grid_width
        elif direction == Buttons.right:
            self.__state['x'] = (x + 1) % self.__grid_width
        elif direction == Buttons.up:
            self.__state['y'] = (y - 1) % self.__grid_height
        elif direction == Buttons.down:
            self.__state['y'] = (y + 1) % self.__grid_height

    def view(self, screen):
        highlighted_y = self.__state.get('y', 0)
        highlighted_x = self.__state.get('x', 0)

        for x in range(0, self.__grid_width):
            for y in range(0, self.__grid_height):
                if x == highlighted_x and y == highlighted_y:
                    screen.set_cell_color(0, (x, y), (250, 0, 0))
