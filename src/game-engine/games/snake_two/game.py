from engine.input import Buttons
import random
import enum


class SnakeTwoGame:
    def __init__(self, config):
        self.__config = config
        self.__state = InitializeState(self.__config)

    def update(self, player):
        self.__state = self.__state.update(player)

    def view(self, screen):
        self.__state.view(screen)


class PlayerStatus(enum.IntEnum):
    alive = 1
    dead = 2


class PlayerData:
    def __init__(self, config, color, start_x, start_direction):
        self.color = color
        self.snake = [(start_x, config.pair.grid_height / 2), (start_x, config.pair.grid_height / 2 - 1)]
        self.direction = start_direction
        self.status = PlayerStatus.alive

    def view(self, screen):
        for (x, y) in self.snake:
            screen.set_cell_color(0, (x, y), self.color)


class GameData:
    def __init__(self, config):
        self.__grid_width = config.pair.grid_width
        self.__grid_height = config.pair.grid_height
        self.candy_color = (250, 0, 0)
        self.candy = None
        self.possible_candy_positions = []
        self.candy_current_index = 0
        self.players_data = [
            PlayerData(config, (250, 250, 0), 3, Buttons.up),
            PlayerData(config, (250, 0, 250), 8, Buttons.down),
        ]

    def view(self, screen):
        # store the coords of the second view
        # to make sure we draw apples in possible positions
        if self.candy is None:
            self.set_possible_candy_positions(screen)
            self.generate_candy()

        # draw apple
        screen.set_cell_color(1, self.candy, self.candy_color)

        # draw players
        for player_data in self.players_data:
            player_data.view(screen)

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
        if players[0].input.is_any_button_pressed():
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
        self.__update_player(players[0], self.__data.players_data[0])
        self.__update_player(players[1], self.__data.players_data[1])

        # check if we hit each other after the update tick
        # this makes it fair instead of player 1 winning if they both collide
        self.__check_collision(self.__data.players_data[0], self.__data.players_data[1])
        self.__check_collision(self.__data.players_data[1], self.__data.players_data[0])

        if self.__someone_died():
            return GameOverState(self.__config, self.__data)

        return self

    def view(self, screen):
        self.__data.view(screen)

    def __update_player(self, player, player_data):
        direction = player.input.get_direction()
        if direction is not None:
            move = [player_data.direction, direction]
            move.sort()
            if move not in self.invalid_moves:
                player_data.direction = direction

        snake_head = player_data.snake[-1]
        if player_data.direction == Buttons.left:
            self.__move_to(player_data, snake_head[0] - 1, snake_head[1])
        elif player_data.direction == Buttons.up:
            self.__move_to(player_data, snake_head[0], snake_head[1] - 1)
        elif player_data.direction == Buttons.right:
            self.__move_to(player_data, snake_head[0] + 1, snake_head[1])
        elif player_data.direction == Buttons.down:
            self.__move_to(player_data, snake_head[0], snake_head[1] + 1)

    def __check_collision(self, player_from, player_to):
        snake_head = player_from.snake[-1]
        if snake_head in player_to.snake:
            player_from.status = PlayerStatus.dead

    def __someone_died(self):
        for player_data in self.__data.players_data:
            if player_data.status == PlayerStatus.dead:
                return True

        return False

    def __move_to(self, player_data, x, y):
        new_x = x % self.__config.pair.grid_width
        new_y = y % self.__config.pair.grid_height
        coord = (new_x, new_y)

        if coord == self.__data.candy:
            player_data.snake.insert(0, player_data.snake[0])
            player_data.snake.insert(0, player_data.snake[0])
            self.__data.generate_candy()

        # Make us shrink before we go to the next place
        player_data.snake.pop(0)

        # Check if we hit ourselves
        if coord in player_data.snake:
            player_data.status = PlayerStatus.dead

        player_data.snake.append(coord)


class GameOverState:
    def __init__(self, config, data):
        self.__config = config
        self.__data = data
        self.__grid_width = config.pair.grid_width
        self.__grid_height = config.pair.grid_height
        self.__y = 0
        self.__color = self.__get_winner_color()

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
                screen.set_cell_color(0, (x, y), self.__color)

    def __get_winner_color(self):
        player_one_status = self.__data.players_data[0].status
        player_two_status = self.__data.players_data[1].status

        if player_one_status == PlayerStatus.alive and player_two_status == PlayerStatus.dead:
            return self.__data.players_data[0].color
        elif player_one_status == PlayerStatus.dead and player_two_status == PlayerStatus.alive:
            return self.__data.players_data[1].color
        else:
            return (250, 0, 0)


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


