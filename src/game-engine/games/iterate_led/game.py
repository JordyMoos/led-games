import random
import time


class IterateLedGame:
    def __init__(self, config):
        self.__total_leds = config.led.total
        self.__led_index = 0
        # self.start = -50

    def update(self, players):
        self.__led_index = (self.__led_index + 10) % self.__total_leds

        # self.start += 50
        # time.sleep(3)
        # print(self.start)

    def view(self, screen):
        # for x in range(self.start, self.start + 50):
        #     screen.set_led_color(x, 150, 0, 0)
        screen.set_led_color(self.__led_index, 30, 0, 0)

