from engine.text import TextCreator
import datetime
import random
import time


class NewYearGame:
    def __init__(self, config):
        self.__config = config
        self.__state = PulseGameState(self.__config)
        # self.__state = CountdownGameState(self.__config)
        # self.__state = TwentyTwentyGameState(self.__config)
        # self.__state = FireworkGameState(self.__config)

    def update(self, players):
        self.__state = self.__state.update(players)

    def view(self, screen):
        self.__state.view(screen)


class PulseGameState:
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
            return PreCountdownGameState(self.__config)

        for led_index, pulse_color in self.__leds.items():
            pulse_color.update()

        return self

    def view(self, screen):
        for led_index, pulse_color in self.__leds.items():
            color = pulse_color.color()
            screen.set_led_color(led_index, color[0], color[1], color[2])


class PreCountdownGameState:
    def __init__(self, config):
        self.__config = config
        self.__leds = {}

        led_percentage = 20
        for led_index in range(0, self.__config.led.total):
            if random.randrange(0, 100) <= led_percentage:
                self.__leds[led_index] = PulseColor(Color.random_color(), speed=10)

    def update(self, players):
        second = datetime.datetime.now().second
        if second > 49:
            return CountdownGameState(self.__config)

        for led_index, pulse_color in self.__leds.items():
            pulse_color.update()

        return self

    def view(self, screen):
        for led_index, pulse_color in self.__leds.items():
            color = pulse_color.color()
            screen.set_led_color(led_index, color[0], color[1], color[2])


class CountdownGameState:
    def __init__(self, config):
        self.__config = config
        self.__text_creator = TextCreator()
        self.__text = None

    def update(self, players):
        # Check if time is past, than return firework state
        minute = datetime.datetime.now().minute
        if minute % 2 == 0:
            return TwentyTwentyGameState(self.__config)

        seconds_left = 60 - datetime.datetime.now().second
        self.__text = self.__text_creator.string_to_letters(str(seconds_left))

        if seconds_left < 10:
            self.__text.set_scale(6)
        else:
            self.__text.set_scale(3)

        return self

    def view(self, screen):
        if not self.__text:
            return

        self.__text.draw(screen, (250, 0, 0), 50, 60)


class TwentyTwentyGameState:
    def __init__(self, config):
        self.__config = config
        self.__text_creator = TextCreator()

        self.__delay_until = time.time() + 5
        self.__text = self.__text_creator.string_to_letters(str("20"))
        self.__text.set_scale(4)

    def update(self, players):
        if self.__delay_until <= time.time():
            return FireworkGameState(self.__config)

        return self

    def view(self, screen):
        self.__text.draw(screen, Color.random_color(maximum=100), 50, 60)


class BigBangGameState:
    def __init__(self, config):
        self.__config = config
        self.__grid_width = config.pair.grid_width
        self.__grid_height = config.pair.grid_height
        self.__y = self.__grid_height + 1

    def update(self, players):
        if self.__y == 0:
            return FireworkGameState(self.__config)

        self.__y = max(self.__y - 2, 0)

        return self

    def view(self, screen):
        for x in range(0, self.__grid_width):
            for y in range(self.__y, self.__grid_height):
                screen.set_cell_color(0, (x, y), (250, 0, 0))


class FireworkGameState:
    def __init__(self, config):
        self.__config = config
        self.__grid_width = config.pair.grid_width
        self.__grid_height = config.pair.grid_height

        self.__fireworks = [Firework(self.__config, x) for x in range(1, self.__grid_width, 1)]

    def update(self, players):
        for firework in self.__fireworks:
            firework.update()

        return self

    def view(self, screen):
        for firework in self.__fireworks:
            firework.view(screen)


class Firework:
    def __init__(self, config, x):
        self.__config = config
        self.__x = x
        self.__state = FireworkDelayState(config, x)

    def update(self):
        self.__state = self.__state.update()

    def view(self, screen):
        self.__state.view(screen)


class FireworkDelayState:
    def __init__(self, config, x):
        self.__config = config
        self.__x = x
        self.__delay_until = time.time() + (random.randrange(500, 8000, 100) / 1000)

    def update(self):
        if self.__delay_until <= time.time():
            return FireworkShootState(self.__config, self.__x)

        return self

    def view(self, screen):
        pass


class FireworkShootState:
    def __init__(self, config, x):
        self.__config = config
        self.__x = x
        self.__grid_height = self.__config.pair.grid_height
        self.__y = self.__grid_height
        self.__y_min = round(self.__grid_height / 100 * random.randrange(10, 80, 5))

    def update(self):
        if self.__y < self.__y_min:
            return FireworkBangState(self.__config, self.__x, self.__y)

        self.__y -= 2

        return self

    def view(self, screen):
        for y in range(self.__y, min(self.__grid_height, self.__y + 4)):
            screen.set_cell_color(0, (self.__x, y), (250, 50, 0))


class FireworkBangState:
    def __init__(self, config, x, y):
        self.__config = config
        self.__x = x
        self.__y = y
        self.__delay_until = time.time() + (random.randrange(800, 3000, 100) / 1000)

        color = Color.random_color()
        self.__glitters = []
        self.__glitters.append(Glitter(self.__x, self.__y, color))
        for x in range(self.__x - 1, self.__x + 2):
            self.__glitters.append(Glitter(x, self.__y + 1, color))
        for x in range(self.__x - 2, self.__x + 3):
            self.__glitters.append(Glitter(x, self.__y + 2, color))
        for x in range(self.__x - 1, self.__x + 2):
            self.__glitters.append(Glitter(x, self.__y + 3, color))

    def update(self):
        if self.__delay_until < time.time():
            return FireworkDelayState(self.__config, self.__x)

        for glitter in self.__glitters:
            glitter.update()

        return self

    def view(self, screen):
        for glitter in self.__glitters:
            glitter.view(screen)


class Glitter:
    def __init__(self, x, y, color):
        self.__x = x
        self.__y = y
        self.__pulse_color = PulseColor(color, 50, 250)

    def update(self):
        self.__pulse_color.update()

    def view(self, screen):
        screen.set_cell_color(0, (self.__x, self.__y), self.__pulse_color.color())


# Should be refactored with the pulse of pulse game
class PulseColor:
    def __init__(self, color, speed = 1, max = 100):
        self.__max_red = color[0]
        self.__max_green = color[1]
        self.__max_blue = color[2]
        self.__speed = speed
        self.__max = max
        self.__direction = random.randrange(-1, 2, 2) + self.__speed
        self.__status = random.randrange(1, self.__max + 1)

    def update(self):
        self.__status = max(min(self.__status + self.__direction, 255), 0)
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


class Color:
    @staticmethod
    def random_color(maximum=250):
        maximum = min(250, maximum)
        red = 0
        green = 0
        blue = 0
        colors = random.randrange(1, 8)
        if 1 & colors:
            red = random.randrange(1, maximum)
        if 2 & colors:
            green = random.randrange(1, maximum)
        if 4 & colors:
            blue = random.randrange(1, maximum)

        return (red, green, blue)
