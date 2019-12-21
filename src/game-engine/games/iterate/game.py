import random


class IterateGame:
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
        self.__state['x'] = (x + 1) % self.__grid_width
        self.__state['y'] = (y + 1) % self.__grid_height

    def view(self, screen):
        highlighted_y = self.__state.get('y', 0)
        highlighted_x = self.__state.get('x', 0)

        colors = random.randrange(1, 8)
        red = 0
        green = 0
        blue = 0
        if 1 & colors:
            red = random.randrange(1, 200, 10)
        if 2 & colors:
            green = random.randrange(1, 200, 10)
        if 4 & colors:
            blue = random.randrange(1, 200, 10)

        for x in range(0, self.__grid_width):
            for y in range(0, self.__grid_height):
                if y == highlighted_y or x == highlighted_x:
                    screen.set_cell_color(0, (x, y), (red, green, blue))
