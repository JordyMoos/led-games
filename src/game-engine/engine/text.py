
class TextCreator:
    # Design = List Int
    # dictionary = Dict Char Design
    dictionary = {
        'a': [" o ",
              "o o",
              "ooo",
              "o o",
              "o o"],
        'b': ["oo ",
              "o o",
              "oo ",
              "o o",
              "oo "],
        'c': [" oo",
              "o  ",
              "o  ",
              "o  ",
              " oo"],
        'd': ["oo ",
              "o o",
              "o o",
              "o o",
              "oo "],
        'e': ["oo",
              "o ",
              "oo",
              "o ",
              "oo"],
        'f': ["oo",
              "o ",
              "oo",
              "o ",
              "o "],
        'g': [" ooo",
              "o  ",
              "o oo",
              "o  o",
              " oo "],
        'h': ["o o",
              "o o",
              "ooo",
              "o o",
              "o o"],
        'i': ["o",
              "o",
              "o",
              "o",
              "o"],
        'j': ["  o",
              "  o",
              "  o",
              "o o",
              " o"],
        'k': ["o  o",
              "o o ",
              "oo  ",
              "o o ",
              "o  o"],
        'l': ["o ",
              "o ",
              "o ",
              "o ",
              "oo"],
        'm': ["o   o",
              "oo oo",
              "o o o",
              "o   o",
              "o   o"],
        'n': ["o   o",
              "oo  o",
              "o o o",
              "o  oo",
              "o   o"],
        'o': [" oo ",
              "o  o",
              "o  o",
              "o  o",
              " oo "],
        'p': ["oo ",
              "o o",
              "oo ",
              "o  ",
              "o  "],
        'q': [" oo",
              "o o",
              " oo",
              "  o",
              "  o"],
        'r': ["oo ",
              "o o",
              "oo ",
              "o o",
              "o o"],
        's': [" oo",
              "o  ",
              " oo",
              "  o",
              "oo "],
        't': ["ooo",
              " o ",
              " o ",
              " o ",
              " o "],
        'u': ["o o",
              "o o",
              "o o",
              "o o",
              "ooo"],
        'v': ["o o",
              "o o",
              "o o",
              "o o",
              " o "],
        'w': ["o   o",
              "o o o",
              "o o o",
              "oo oo",
              "o   o"],
        'x': ["o o",
              "o o",
              " o ",
              "o o",
              "o o"],
        'y': ["o o",
              "o o",
              " o ",
              " o ",
              " o "],
        'z': ["ooo",
              "  o",
              " o ",
              "o  ",
              "ooo"],
        '0': [" o ",
              "o o",
              "o o",
              "o o",
              " o "],
        '1': ["  o",
              "  o",
              "  o",
              "  o",
              "  o"],
        '2': [" o ",
              "o o",
              "  o",
              " o ",
              "ooo"],
        '3': ["ooo",
              "  o",
              " oo",
              "  o",
              "oo "],
        '4': ["o o",
              "o o",
              "ooo",
              "  o",
              "  o"],
        '5': ["ooo",
              "o  ",
              "oo ",
              "  o",
              "oo "],
        '6': ["o  ",
              "o  ",
              "ooo",
              "o o",
              "ooo"],
        '7': ["ooo",
              "  o",
              "  o",
              "  o",
              "  o"],
        '8': ["ooo",
              "o o",
              "ooo",
              "o o",
              "ooo"],
        '9': ["ooo",
              "o o",
              "ooo",
              "  o",
              "ooo"],
        ' ': [" ",
              " ",
              " ",
              " ",
              " "],
        '.': [" ",
              " ",
              " ",
              " ",
              "o"],
        ':': [" ",
              "o",
              " ",
              " ",
              "o"],
        '=': ["   ",
              "ooo",
              "   ",
              "ooo",
              "   "],
        ',': ["  ",
              "  ",
              "  ",
              " o",
              "o "],
        '-': ["  ",
              "  ",
              "oo",
              "  ",
              "  "],
        '[': ["oo",
              "o ",
              "o ",
              "o ",
              "oo"],
        ']': ["oo",
              " o",
              " o",
              " o",
              "oo"]
    }

    def __init__(self):
        self.letters = {char: TextCreator.__design_to_letter(design) for char, design in TextCreator.dictionary.items()}

    def string_to_letters(self, string):
        return Text([self.letters.get(char) for char in string.lower() if self.letters.get(char)])

    @staticmethod
    def __get_width(design):
        return max([len(line) for line in design])

    @staticmethod
    def __get_height(design):
        return len(design)

    @staticmethod
    def __get_positions(design):
        positions = []
        for y, line in enumerate(design):
            for x, char in enumerate(line):
                if char is not ' ':
                    positions.append({
                        'x': x,
                        'y': y
                    })
        return positions

    @staticmethod
    def __design_to_letter(design):
        return Letter(
            TextCreator.__get_width(design),
            TextCreator.__get_height(design),
            TextCreator.__get_positions(design)
        )


class Text:
    def __init__(self, letters):
        self.__letters = letters
        self.__spacing = 1

    def draw(self, screen, start_x, start_y):
        for letter in self.__letters:
            letter.draw(screen, start_x, start_y)
            start_x += letter.width + self.__spacing


class Letter:
    def __init__(self, width, height, positions):
        self.__width = width
        self.__height = height
        self.__positions = positions
        self.__color = (255, 0, 0)
        self.__view_index = 0

    def draw(self, screen, start_x, start_y):
        for position in self.__positions:
            coord = (position['x'] + start_x, position['y'] + start_y)
            screen.set_cell_color(self.__view_index, coord, self.__color)

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def positions(self):
        return self.__positions
