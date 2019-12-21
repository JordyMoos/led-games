from engine.input import Buttons
import random


class SnakeGame:
    def __init__(self, config):
        self.__config = config
        self.__state = InitializeState(self.__config)

    def update(self, players):
        self.__state = self.__state.update(players)

    def view(self, screen):
        self.__state.view(screen)


class GameData:
    def __init__(self, config):
        self.__grid_width = config.pair.grid_width
        self.__grid_height = config.pair.grid_height
        self.snake = [(3, config.pair.grid_height), (3, config.pair.grid_height - 1)]
        self.direction = Buttons.up
        self.candy = None
        self.possible_candy_positions = []
        self.candy_current_index = 0

    def view(self, screen):
        # store the coords of the second view
        # to make sure we draw apples in possible positions
        if self.candy is None:
            self.set_possible_candy_positions(screen)
            self.generate_candy()

        # draw apple
        screen.set_cell_color(1, self.candy, (0, 0, 250))

        # draw snake
        for (x, y) in self.snake:
            screen.set_cell_color(0, (x, y), (250, 0, 0))

    def generate_candy(self):
        self.candy_current_index = (self.candy_current_index + 1) % len(self.possible_candy_positions)
        self.candy = self.possible_candy_positions[self.candy_current_index]

    def set_possible_candy_positions(self, screen):
        self.possible_candy_positions = list(screen.get_view(1).keys())
        random.shuffle(self.possible_candy_positions)
        self.candy_current_index = 0


class InitializeState:
    def __init__(self, config):
        self.__config = config
        self.__data = GameData(config)

    def update(self, players):
        return WaitingForInputState(self.__config, self.__data)

    def view(self, screen):
        self.__data.view(screen)


class WaitingForInputState:
    def __init__(self, config, data):
        self.__config = config
        self.__data = data

    def update(self, players):
        player = players[0]
        if player.input.is_any_button_pressed():
            return PlayingState(self.__config, self.__data)

        return self

    def view(self, screen):
        self.__data.view(screen)


class PlayingState:
    invalid_moves = [[Buttons.left, Buttons.right], [Buttons.up, Buttons.down]]

    def __init__(self, config, data):
        self.__config = config
        self.__data = data

    def update(self, players):
        player = players[0]
        direction = player.input.get_direction()
        if direction is not None:
            move = [self.__data.direction, direction]
            move.sort()
            if move not in self.invalid_moves:
                self.__data.direction = direction

        snake_head = self.__data.snake[-1]
        if self.__data.direction == Buttons.left:
            return self.__move_to(snake_head[0] - 1, snake_head[1])
        elif self.__data.direction == Buttons.up:
            return self.__move_to(snake_head[0], snake_head[1] - 1)
        elif self.__data.direction == Buttons.right:
            return self.__move_to(snake_head[0] + 1, snake_head[1])
        elif self.__data.direction == Buttons.down:
            return self.__move_to(snake_head[0], snake_head[1] + 1)

        return self

    def view(self, screen):
        self.__data.view(screen)

    def __move_to(self, x, y):
        new_x = x % self.__config.pair.grid_width
        new_y = y % self.__config.pair.grid_height
        coord = (new_x, new_y)

        if coord == self.__data.candy:
            self.__data.snake.insert(0, self.__data.snake[0])
            self.__data.generate_candy()

        # Make us shrink before we go to the next place
        self.__data.snake.pop(0)

        # Check if we hit ourselves
        if coord in self.__data.snake:
            return GameOverState(self.__config, self.__data)

        self.__data.snake.append(coord)

        return self


class GameOverState:
    def __init__(self, config, data):
        self.__config = config
        self.__data = data
        self.__grid_width = config.pair.grid_width
        self.__grid_height = config.pair.grid_height
        self.__y = 0

    def update(self, players):
        if self.__y < self.__grid_height:
            self.__y = self.__y + 1
        else:
            return InitializeState(self.__config)

        return self

    def view(self, screen):
        self.__data.view(screen)

        for y in range(0, self.__y):
            for x in range(0, self.__grid_width):
                screen.set_cell_color(0, (x, y), (50, 0, 0))


# Not implemented yet
class ShowScoreState:
    def __init__(self, config, data):
        self.__config = config
        self.__data = data
        pass

    def update(self, players):
        return self

    def view(self, screen):
        pass


