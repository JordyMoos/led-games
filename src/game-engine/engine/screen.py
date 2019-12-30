import math
import random


class Screen:
    def __init__(self, config, views, led_pixels):
        self.__config = config
        self.__max_brightness = self.__config.led.max_brightness
        self.__views = views
        self.__led_pixels = led_pixels
        self.__physical_leds = []
        self.clear()

    @property
    def views(self):
        return self.__views

    @property
    def grid_width(self):
        return self.__config.pair.grid_width

    @property
    def grid_height(self):
        return self.__config.pair.grid_height

    def get_view(self, view_index=1):
        return self.__views[view_index]

    def set_cell_color(self, view_index, coord, rgb):
        red = self.__calc_color(rgb[0])
        green = self.__calc_color(rgb[1])
        blue = self.__calc_color(rgb[2])
        for led_index in self.__views[view_index].get(coord, []):
            self.set_led_color(led_index, red, green, blue)

    def __calc_color(self, color):
        return color  # math.floor(color / 255 * 50)

    @property
    def led_pixels(self):
        return self.__led_pixels

    @property
    def physical_leds(self):
        return self.__physical_leds

    def clear(self):
        self.__physical_leds = [0, 0, 0] * self.__config.led.total

    def set_led_color(self, index, red, green, blue):
        key = index * 3
        self.__physical_leds[key] = round(red / 255 * self.__max_brightness)
        self.__physical_leds[key + 1] = round(green / 255 * self.__max_brightness)
        self.__physical_leds[key + 2] = round(blue / 255 * self.__max_brightness)


class ScreenProvider:
    @staticmethod
    def create(config):
        # type alias LedIndex = Int
        # type alias X = Int
        # type alias Y = Int
        # lines: List (IndexId, X, Y)
        lines = ScreenProvider.__read_pair_file(config.pair.pair_file)
        views_indices = [ScreenProvider.__read_view_file(view_file) for view_file in config.pair.view_files]

        # List(Dict (X, Y) (List LedIndex))
        views = [{} for _ in views_indices]

        # type alias PixelX = Int
        # type alias PixelY = Int
        # Dict LedIndex (PixelX, PixelY)
        led_pixels = {}

        for line in lines:
            if config.pair.min_x <= line[1] <= config.pair.max_x:
                if config.pair.min_y <= line[2] <= config.pair.max_y:
                    led_index = line[0]
                    led_pixel_x = line[1] - config.pair.min_x
                    led_pixel_y = line[2] - config.pair.min_y
                    led_grid_x = math.floor(led_pixel_x / config.pair.grid_width_pixels)
                    led_grid_y = math.floor(led_pixel_y / config.pair.grid_height_pixels)
                    led_grid_cell = (led_grid_x, led_grid_y)

                    led_pixels[led_index] = (led_pixel_x, led_pixel_y)

                    # Weird mutable language...
                    # grid_led_indices = led_grid.get(led_grid_cell, [])
                    # grid_led_indices.append(led_index)
                    # led_grid[led_grid_cell] = grid_led_indices
                    for view_index in range(len(views)):
                        if led_index in views_indices[view_index]:
                            view_led_indices = views[view_index].get(led_grid_cell, [])
                            view_led_indices.append(led_index)
                            views[view_index][led_grid_cell] = view_led_indices

        limited_views = [{} for _ in views_indices]
        for view_index in range(len(views)):
            limited_view = {}
            for cell, led_indices in views[view_index].items():
                random.shuffle(led_indices)
                limited_view[cell] = led_indices[:config.led.per_cell]
            limited_views[view_index] = limited_view

        return Screen(config, limited_views, led_pixels)

    @staticmethod
    def __read_pair_file(file):
        return [
            list(map(int, line.rstrip('\n').split(',', 3)))
            for line in open(file)
        ]

    @staticmethod
    def __read_view_file(file):
        return [
            int(line.rstrip('\n'))
            for line in open(file)
        ]



