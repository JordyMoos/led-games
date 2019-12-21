from engine.input import Buttons
import itertools
import random
import math
import time

'''

Tic Tac Toe implemented by a magic square.

This is probably the worst implementation ever but I always wanted to
apply a magic square to a game and Tic Tac Toe looks like a perfect fit.

The magic square for Tic Tac Toe is:
[2, 7, 6
,9, 5, 1
,4, 3, 8]

The whole idea with magic squares is that sums of all the rows (straight and diagional)
will result in the same number. Which in this case is 15.

Therefor checking if a player has won, "is as simple as" checking if the sum of three of their chosen
positions is equal to 15.

'''

DRAW_COLOR = 250, 0, 0
GAME_GRID = [2, 7, 6, 9, 5, 1, 4, 3, 8]


class TicTacToe:
    def __init__(self, config):
        if config.pair.grid_width < 3:
            exit("The grid is not width enough to play Tic Tac Toe")
        elif config.pair.grid_height < 3:
            exit("The grid is not high enough to play Tic Tac Toe")

        self.__config = config
        self.__state = PlayingState(self.__config)

    def update(self, players):
        self.__state = self.__state.update(players)

    def view(self, screen):
        self.__state.view(screen)


class Pointer:
    def __init__(self, config, color):
        self.__grid_width = config.pair.grid_width
        self.__grid_height = config.pair.grid_height
        self.x = 1
        self.y = 1
        self.pulse = PulseState(color)

    def update(self):
        self.pulse.update()

    def move(self, direction):
        if direction == Buttons.left:
            self.x = (self.x - 1) % 3
        elif direction == Buttons.right:
            self.x = (self.x + 1) % 3
        elif direction == Buttons.up:
            self.y = (self.y - 1) % 3
        elif direction == Buttons.down:
            self.y = (self.y + 1) % 3

    def position(self):
        return self.x + (self.y * 3)

    def view(self, screen):
        for x in range(0, self.__grid_width):
            x_offset = math.floor(x / self.__grid_width * 3)
            for y in range(0, self.__grid_height):
                y_offset = math.floor(y / self.__grid_height * 3) * 3
                total_offset = x_offset + y_offset

                if self.position() == total_offset:
                    screen.set_cell_color(0, (x, y), self.pulse.color())


class PlayerData:
    def __init__(self, config, color):
        self.__grid_width = config.pair.grid_width
        self.__grid_height = config.pair.grid_height
        self.color = color
        self.positions = []

    def claim(self, magic_number):
        self.positions.append(magic_number)

    def has_won(self):
        return bool(self.get_winning_lines())

    def get_winning_lines(self):
        return [combination for combination in itertools.combinations(self.positions, 3)
                    if len(combination) == 3 and sum(combination) == 15]

    def view(self, screen):
        for x in range(0, self.__grid_width):
            x_offset = math.floor(x / self.__grid_width * 3)
            for y in range(0, self.__grid_height):
                y_offset = math.floor(y / self.__grid_height * 3) * 3
                total_offset = x_offset + y_offset
                magic_number = GAME_GRID[total_offset]

                if magic_number in self.positions:
                    screen.set_cell_color(0, (x, y), self.color)


class PlayingState:
    def __init__(self, config):
        self.__config = config
        self.__players = [
            PlayerData(config, (250, 250, 0)),
            PlayerData(config, (250, 0, 250)),
        ]
        self.__current_player_index = random.randrange(0, 2)
        self.__delay_until = time.time() + 0.5
        self.__init_pointer()

    def update(self, players):
        if not self.__has_possible_positions():
            return GameOverState(self.__config, DRAW_COLOR)

        self.pointer.update()

        return self.__handle_turn(
            players[self.__current_player_index]
        )

    def view(self, screen):
        # draw players
        for player_data in self.__players:
            player_data.view(screen)

        # draw pointer
        self.pointer.view(screen)

    def __possible_magic_numbers(self):
        taken_positions = [player.positions for player in self.__players]
        merged_positions = list(itertools.chain(*taken_positions))

        return list(set(GAME_GRID) - set(merged_positions))

    def __has_possible_positions(self):
        return bool(self.__possible_magic_numbers())

    def __handle_turn(self, player_input):
        current_time = time.time()
        if current_time < self.__delay_until:
            return self

        direction = player_input.input.get_direction()
        if direction:
            self.pointer.move(direction)
            self.__delay_until = time.time() + 0.2
            return self

        if player_input.input.is_pressed(Buttons.ok):
            current_magic_number = GAME_GRID[self.pointer.position()]
            if current_magic_number in self.__possible_magic_numbers():
                self.__players[self.__current_player_index].claim(current_magic_number)
                if self.__players[self.__current_player_index].has_won():
                    return GameOverState(
                        self.__config,
                        self.__players[self.__current_player_index].color
                    )
                self.__delay_until = time.time() + 0.2
                self.__current_player_index = (self.__current_player_index + 1) % 2
                self.__init_pointer()

        return self

    def __init_pointer(self):
        self.pointer = Pointer(self.__config,
                               self.__players[self.__current_player_index].color)


class GameOverState:
    def __init__(self, config, color):
        self.__config = config
        self.__color = color
        self.__grid_width = config.pair.grid_width
        self.__grid_height = config.pair.grid_height
        self.__y = 0
        self.__delay_until = time.time() + 0.5

    def update(self, players):
        current_time = time.time()
        if current_time < self.__delay_until:
            return self

        if players[0].input.is_any_button_pressed():
            return PlayingState(self.__config)

        if self.__y < self.__grid_height:
            self.__y = self.__y + 1

        return self

    def view(self, screen):
        for y in range(0, self.__y):
            for x in range(0, self.__grid_width):
                screen.set_cell_color(0, (x, y), self.__color)


# Should be refactored with the pulse of pulse game
class PulseState:
    def __init__(self, color):
        self.__max_red = color[0]
        self.__max_green = color[1]
        self.__max_blue = color[2]
        self.__max = 100
        self.__direction = random.randrange(-1, 2, 2) * 20
        self.__status = random.randrange(1, self.__max + 1)

    def update(self):
        self.__status = self.__status + self.__direction
        if self.__status < 1:
            self.__status = 1
            self.__direction = self.__direction * -1
        elif self.__status > self.__max:
            self.__status = self.__max
            self.__direction = self.__direction * -1

    def color(self):
        return (int(self.__max_red * (self.__status / self.__max)) + 1,
                int(self.__max_green * (self.__status / self.__max)) + 1,
                int(self.__max_blue * (self.__status / self.__max)) + 1,
                )
