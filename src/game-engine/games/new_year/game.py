from engine.text import TextCreator
import datetime


class SnakeGame:
    def __init__(self, config):
        self.__config = config
        self.__state = InitializeState(self.__config)

    def update(self, players):
        self.__state = self.__state.update(players)

    def view(self, screen):
        self.__state.view(screen)


class InitializeState:
    def __init__(self, config):
        self.__config = config

    def update(self, players):
        return WaitingForInputState(self.__config, self.__data)

    def view(self, screen):
        self.__data.view(screen)


class WaitingForInputState:
    def __init__(self, config, data):
        self.__config = config
        self.__data = data

    def update(self, players):
        player = players[0]
        if player.input.is_any_button_pressed():
            return PlayingState(self.__config, self.__data)

        return self

    def view(self, screen):
        self.__data.view(screen)


class CountdownState:
    def __init__(self, config):
        self.__config = config
        self.__text_creator = TextCreator()
        self.__text = None

    def update(self, players):
        # Check if time is past, than return firework state

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



class GameOverState:
    def __init__(self, config, data):
        self.__config = config
        self.__data = data
        self.__grid_width = config.pair.grid_width
        self.__grid_height = config.pair.grid_height
        self.__y = 0

    def update(self, players):
        if self.__y < self.__grid_height:
            self.__y = self.__y + 1
        else:
            return InitializeState(self.__config)

        return self

    def view(self, screen):
        self.__data.view(screen)

        for y in range(0, self.__y):
            for x in range(0, self.__grid_width):
                screen.set_cell_color(0, (x, y), (50, 0, 0))

