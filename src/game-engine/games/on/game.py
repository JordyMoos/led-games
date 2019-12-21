
class AllOnGame:
    def __init__(self, config):
        self.__grid_width = config.pair.grid_width
        self.__grid_height = config.pair.grid_height

    def update(self, players):
        pass

    def view(self, screen):
        for x in range(0, self.__grid_width):
            for y in range(0, self.__grid_height):
                screen.set_cell_color(1, (x, y), (0, 0, 250))

