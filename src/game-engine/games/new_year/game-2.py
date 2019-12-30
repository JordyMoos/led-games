from engine.text import TextCreator
import datetime


class NewYearGame:
    def __init__(self, config):
        self.__config = config
        self.__text_creator = TextCreator()
        self.__text = None

    def update(self, players):
        seconds_left = 60 - datetime.datetime.now().second
        self.__text = self.__text_creator.string_to_letters(str(seconds_left))

        if seconds_left < 10:
            self.__text.set_scale(3)
        else:
            self.__text.set_scale(2)

    def view(self, screen):
        if not self.__text:
            return

        self.__text.draw(screen, 50, 40)
