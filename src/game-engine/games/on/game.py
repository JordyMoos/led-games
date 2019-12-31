
class AllOnGame:
    def __init__(self, config):
        self.__total = config.led.total

    def update(self, players):
        pass

    def view(self, screen):
        for index in range(0, self.__total):
            screen.set_led_color(index, 100, 0, 0)


