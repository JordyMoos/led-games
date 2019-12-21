from games.pulse.pulse_state import PulseState


class PulseGame:
    def __init__(self, config, color_type):
        self.__grid_width = config.pair.grid_width
        self.__grid_height = config.pair.grid_height
        self.__state = {}

        for x in range(0, self.__grid_width):
            for y in range(0, self.__grid_height):
                self.__state[(x, y)] = PulseState(color_type)

    def update(self, players):
        for x in range(0, self.__grid_width):
            for y in range(0, self.__grid_height):
                self.__state[(x, y)].update()

    def view(self, screen):
        for x in range(0, self.__grid_width):
            for y in range(0, self.__grid_height):
                screen.set_cell_color(0, (x, y), self.__state[(x, y)].color())
