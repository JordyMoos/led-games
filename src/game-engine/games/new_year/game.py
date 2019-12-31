from engine.text import TextCreator
import datetime


class NewYearGame:
    def __init__(self, config):
        self.__config = config
        self.__state = CountdownState(self.__config)

    def update(self, players):
        self.__state = self.__state.update(players)

    def view(self, screen):
        self.__state.view(screen)


class CountdownState:
    def __init__(self, config):
        self.__config = config
        self.__text_creator = TextCreator()
        self.__text = None

    def update(self, players):
        # Check if time is past, than return firework state
        # minute = datetime.datetime.now().minute
        # if minute % 2 == 0:
        #     return BigBangState(self.__config)

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

    def update(self, players):

        return self

    def view(self, screen):
        pass
