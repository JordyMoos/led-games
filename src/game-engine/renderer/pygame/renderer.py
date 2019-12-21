import pygame
import math
from time import sleep


class PyGameRenderer:
    def __init__(self, config):
        self.__config = config

        max_width = 1200
        max_height = 800

        if max_width / self.__config.pair.screen_width_pixels < max_height / self.__config.pair.screen_height_pixels:
            width = max_width
            self.__ratio = width / self.__config.pair.screen_width_pixels
            height = self.__ratio * self.__config.pair.screen_height_pixels
        else:
            height = max_height
            self.__ratio = height / self.__config.pair.screen_height_pixels
            width = self.__ratio * self.__config.pair.screen_width_pixels

        pygame.init()
        self.__screen = pygame.display.set_mode((math.ceil(width), math.ceil(height)))
        pygame.display.set_caption("Led Game Engine")

    def render(self, screen):
        self.__screen.fill(pygame.Color('white'))

        physical_leds = screen.physical_leds
        for led_index, (led_pixel_x, led_pixel_y) in screen.led_pixels.items():
            mapped_index = led_index * 3
            red = physical_leds[mapped_index]
            green = physical_leds[mapped_index + 1]
            blue = physical_leds[mapped_index + 2]
            color = self.__from_rgb(red, green, blue)

            pygame.draw.circle(self.__screen, color, (round(led_pixel_x * self.__ratio), round(led_pixel_y * self.__ratio)), 6)

        pygame.display.flip()
            
    @staticmethod
    def __from_rgb(red, green, blue):
        if not red and not green and not blue:
            return pygame.Color('lightgrey')

        return pygame.Color(red, green, blue)
