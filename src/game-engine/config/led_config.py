
class LedConfig:
    def __init__(self, total, per_cell, max_brightness):
        self.__total = total
        self.__per_cell = per_cell
        self.__max_brightness = max_brightness

    @property
    def total(self):
        return self.__total

    @property
    def per_cell(self):
        return self.__per_cell

    @property
    def max_brightness(self):
        return self.__max_brightness
