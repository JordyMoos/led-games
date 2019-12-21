import random


class PulseState:
    def __init__(self, color_type):
        self.__max_red = 0
        self.__max_green = 0
        self.__max_blue = 0

        if color_type == 'random':
            colors = random.randrange(1, 8)
            if 1 & colors:
                self.__max_red = random.randrange(1, 250, 5)
            if 2 & colors:
                self.__max_green = random.randrange(1, 250, 5)
            if 4 & colors:
                self.__max_blue = random.randrange(1, 250, 5)
        else:
            self.__max_red = 250
            self.__max_green = 50
            self.__max_blue = 0

        self.__max = random.randrange(10, 100, 2)
        self.__direction = random.randrange(-1, 2, 2)
        self.__status = random.randrange(1, self.__max + 1)

    def update(self):
        self.__status = self.__status + self.__direction
        if self.__status < 1:
            self.__status = 1
            self.__direction = 1
        elif self.__status > self.__max:
            self.__status = self.__max
            self.__direction = -1

    def color(self):
        return (int(self.__max_red * (self.__status / self.__max)) + 1,
                int(self.__max_green * (self.__status / self.__max)) + 1,
                int(self.__max_blue * (self.__status / self.__max)) + 1,
                )
