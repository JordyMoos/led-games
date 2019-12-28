from engine.text import TextCreator
import datetime


class NewYearGame:
    def __init__(self, config):
        self.__config = config
        self.__text_creator = TextCreator()

        self.__text = None

    def update(self, players):
        seconds_left = 60 - datetime.datetime.now().second
        self.__text = self.__text_creator.string_to_letters(
            str(seconds_left)
        )

    def view(self, screen):
        if not self.__text:
            return

        self.__text.draw(screen, 2, 8)

