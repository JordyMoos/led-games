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
        '0': ["ooo",
              "o o",
              "o o",
              "o o",
              "ooo"],
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
        self.__scale = 1

    '''
        `horizontal_alignment`
        Can be from 0 to 100.
        Where 0 is left aligned
        50 is centered
        and 100 is right aligned
        
        Same idea for `vertical_alignment`
    '''

    def draw(self, screen, color, horizontal_alignment, vertical_alignment):
        start_x = self.__calculate_start_x(screen, horizontal_alignment)
        start_y = self.__calculate_start_y(screen, vertical_alignment)
        for letter in self.__letters:
            letter.draw(screen, color, self.__scale, start_x, start_y)
            start_x += (letter.width + self.__spacing) * self.__scale

    def set_spacing(self, spacing):
        self.__spacing = spacing

    def set_scale(self, scale):
        self.__scale = max(1, round(scale))

    @property
    def __width(self):
        letters_length = sum([letter.width for letter in self.__letters])
        spacing_length = (len(self.__letters) - 1) * self.__spacing
        return (letters_length + spacing_length) * self.__scale

    @property
    def __height(self):
        return max([letter.height for letter in self.__letters]) * self.__scale

    def __calculate_start_x(self, screen, horizontal_alignment):
        text_width = self.__width
        screen_width = screen.grid_width
        starting_point = round((screen_width - text_width) / 100 * horizontal_alignment)
        return max(0, min(screen_width, starting_point))

    def __calculate_start_y(self, screen, vertical_alignment):
        text_height = self.__height
        screen_height = screen.grid_height
        starting_point = round((screen_height - text_height) / 100 * vertical_alignment)
        return max(0, min(screen_height, starting_point))


class Letter:
    def __init__(self, width, height, positions):
        self.__width = width
        self.__height = height
        self.__positions = positions
        self.__view_index = 0

    def draw(self, screen, color, scale, start_x, start_y):
        for position in self.__positions:
            for x in range(0, scale):
                for y in range(0, scale):
                    coord = (
                        (position['x'] * scale) + x + start_x,
                        (position['y'] * scale) + y + start_y
                    )
                    screen.set_cell_color(self.__view_index, coord, color)

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def positions(self):
        return self.__positions
