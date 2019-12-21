import math


class PairConfig:
    def __init__(self, pair_file, view_files, min_x, max_x, min_y, max_y, grid_width, grid_height):
        self.__pair_file = pair_file
        self.__view_files = view_files
        self.__min_x = min_x
        self.__max_x = max_x
        self.__min_y = min_y
        self.__max_y = max_y
        self.__grid_width = grid_width
        self.__grid_height = grid_height
        self.__screen_width_pixels = self.__max_x - self.__min_x
        self.__screen_height_pixels = self.__max_y - self.__min_y
        self.__grid_width_pixels = math.floor(self.__screen_width_pixels / self.__grid_width)
        self.__grid_height_pixels = math.floor(self.__screen_height_pixels / self.__grid_height)

    @property
    def pair_file(self):
        return self.__pair_file

    @property
    def view_files(self):
        return self.__view_files

    @property
    def min_x(self):
        return self.__min_x

    @property
    def max_x(self):
        return self.__max_x

    @property
    def min_y(self):
        return self.__min_y

    @property
    def max_y(self):
        return self.__max_y

    @property
    def grid_width(self):
        return self.__grid_width

    @property
    def grid_height(self):
        return self.__grid_height

    @property
    def screen_width_pixels(self):
        return self.__screen_width_pixels

    @property
    def screen_height_pixels(self):
        return self.__screen_height_pixels

    @property
    def grid_width_pixels(self):
        return self.__grid_width_pixels

    @property
    def grid_height_pixels(self):
        return self.__grid_height_pixels
