from engine.text import TextCreator
import datetime
import random


class NewYearGame:
    def __init__(self, config):
        self.__config = config
        self.__state = PulseState(self.__config)

    def update(self, players):
        self.__state = self.__state.update(players)

    def view(self, screen):
        self.__state.view(screen)


class PulseState:
    def __init__(self, config):
        self.__config = config
        self.__leds = {}

        led_percentage = 10
        for led_index in range(0, self.__config.led.total):
            if random.randrange(0, 100) <= led_percentage:
                self.__leds[led_index] = PulseColor((250, 50, 0))

    def update(self, players):
        minute = datetime.datetime.now().minute
        if minute % 2 == 1:
            return PreCountdownState(self.__config)

        for led_index, pulse_color in self.__leds.items():
            pulse_color.update()

        return self

    def view(self, screen):
        for led_index, pulse_color in self.__leds.items():
            color = pulse_color.color()
            screen.set_led_color(led_index, color[0], color[1], color[2])


class PreCountdownState:
    def __init__(self, config):
        self.__config = config
        self.__leds = {}

        led_percentage = 20
        for led_index in range(0, self.__config.led.total):
            if random.randrange(0, 100) <= led_percentage:
                red = 0
                green = 0
                blue = 0
                colors = random.randrange(1, 8)
                if 1 & colors:
                    red = random.randrange(1, 250, 5)
                if 2 & colors:
                    green = random.randrange(1, 250, 5)
                if 4 & colors:
                    blue = random.randrange(1, 250, 5)
                self.__leds[led_index] = PulseColor((red, green, blue))

    def update(self, players):
        second = datetime.datetime.now().second
        if second > 30:
            return CountdownState(self.__config)

        for led_index, pulse_color in self.__leds.items():
            pulse_color.update()

        return self

    def view(self, screen):
        for led_index, pulse_color in self.__leds.items():
            color = pulse_color.color()
            screen.set_led_color(led_index, color[0], color[1], color[2])


class CountdownState:
    def __init__(self, config):
        self.__config = config
        self.__text_creator = TextCreator()
        self.__text = None

    def update(self, players):
        # Check if time is past, than return firework state
        minute = datetime.datetime.now().minute
        if minute % 2 == 0:
            return BigBangState(self.__config)

        seconds_left = 60 - datetime.datetime.now().second
        self.__text = self.__text_creator.string_to_letters(str(seconds_left))

        if seconds_left < 10:
            self.__text.set_scale(3)
        else:
            self.__text.set_scale(2)

        return self

    def view(self, screen):
        if not self.__text:
            return

        self.__text.draw(screen, 50, 40)


class BigBangState:
    def __init__(self, config):
        self.__config = config
        self.__grid_width = config.pair.grid_width
        self.__grid_height = config.pair.grid_height
        self.__y = self.__grid_height + 1

    def update(self, players):
        if self.__y == 0:
            return FireworkState(self.__config)

        self.__y = max(self.__y - 2, 0)

        return self

    def view(self, screen):
        for x in range(0, self.__grid_width):
            for y in range(self.__y, self.__grid_height):
                screen.set_cell_color(0, (x, y), (250, 0, 0))


class FireworkState:
    def __init__(self, config):
        self.__config = config
        self.__grid_width = config.pair.grid_width
        self.__grid_height = config.pair.grid_height

    def update(self, players):
        return PulseState(self.__config)

    def view(self, screen):
        pass


# Should be refactored with the pulse of pulse game
class PulseColor:
    def __init__(self, color):
        self.__max_red = color[0]
        self.__max_green = color[1]
        self.__max_blue = color[2]
        self.__max = 100
        self.__direction = random.randrange(-1, 2, 2)
        self.__status = random.randrange(1, self.__max + 1)

    def update(self):
        self.__status = self.__status + self.__direction
        if self.__status < 1:
            self.__status = 1
            self.__direction = self.__direction * -1
        elif self.__status > self.__max:
            self.__status = self.__max
            self.__direction = self.__direction * -1

    def color(self):
        return (int(self.__max_red * (self.__status / self.__max)) + 1,
                int(self.__max_green * (self.__status / self.__max)) + 1,
                int(self.__max_blue * (self.__status / self.__max)) + 1,
                )
