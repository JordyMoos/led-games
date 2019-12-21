class InputGame:
    def __init__(self, config):
        self.__grid_width = config.pair.grid_width
        self.__grid_height = config.pair.grid_height
        self.__view = {}

    def update(self, players):
        x = int(input("X:"))
        if x < 0 or x >= self.__grid_width:
            print("X is out of bound")
            return

        y = int(input("Y:"))
        if x < 0 or x >= self.__grid_height:
            print("Y is out of bound")
            return

        red = min(255, max(0, int(input("Red:"))))
        green = min(255, max(0, int(input("Green:"))))
        blue = min(255, max(0, int(input("Blue:"))))

        self.__view[(x, y)] = (red, green, blue)

        print((red, green, blue))

    def view(self, screen):
        for coord, color in self.__view.items():
            screen.set_cell_color(0, coord, color)

