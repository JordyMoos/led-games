
from games.off.game import AllOffGame
from games.on.game import AllOnGame
from games.pulse.game import PulseGame
from games.input.game import InputGame
from games.iterate.game import IterateGame
from games.move.game import MoveGame
from games.snake.game import SnakeGame
from games.snake_two.game import SnakeTwoGame
from games.tictactoe.game import TicTacToe


class Preset:
    def __init__(self, action, desc):
        self.__action = action
        self.__desc = desc

    @property
    def desc(self):
        return self.__desc

    def create(self, config):
        return self.__action(config)


game_presets = {
    #'screen-recording': Preset((lambda config: ScreenRecordingGame(config)), 'Screen Recording Game'),
    'iterate': Preset((lambda config: IterateGame(config)), 'Iterate through all the leds'),
    'input': Preset((lambda config: InputGame(config)), 'Tell which cell to command'),
    'on': Preset((lambda config: AllOnGame(config)), 'Turn all the leds on'),
    'off': Preset((lambda config: AllOffGame(config)), 'Turn all the leds off'),
    'pulse': Preset((lambda config: PulseGame(config, 'fixed')), 'Pulse the leds in yellow'),
    'pulse-random': Preset((lambda config: PulseGame(config, 'random')), 'Pulse the leds in random colors'),
    'move': Preset((lambda config: MoveGame(config)), 'Move the lines with the controller'),
    'snake': Preset((lambda config: SnakeGame(config)), 'Snake game'),
    'snake-two': Preset((lambda config: SnakeTwoGame(config)), 'Snake multiplayer game'),
    'tictactoe': Preset((lambda config: TicTacToe(config)), 'TicTacToe multiplayer')
}
