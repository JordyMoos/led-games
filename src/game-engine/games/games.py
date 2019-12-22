
from games.off.game import AllOffGame
from games.on.game import AllOnGame
from games.pulse.game import PulseGame
from games.input.game import InputGame
from games.iterate.game import IterateGame
from games.move.game import MoveGame
from games.snake.game import SnakeGame
from games.snake_two.game import SnakeTwoGame
from games.tictactoe.game import TicTacToe


class GameSetup:
    def __init__(self, action, desc):
        self.__action = action
        self.__desc = desc

    @property
    def desc(self):
        return self.__desc

    def create(self, config):
        return self.__action(config)


games = {
    #'screen-recording': Preset((lambda config: ScreenRecordingGame(config)), 'Screen Recording Game'),
    'iterate': GameSetup((lambda config: IterateGame(config)), 'Iterate through all the leds'),
    'input': GameSetup((lambda config: InputGame(config)), 'Tell which cell to command'),
    'on': GameSetup((lambda config: AllOnGame(config)), 'Turn all the leds on'),
    'off': GameSetup((lambda config: AllOffGame(config)), 'Turn all the leds off'),
    'pulse': GameSetup((lambda config: PulseGame(config, 'fixed')), 'Pulse the leds in yellow'),
    'pulse-random': GameSetup((lambda config: PulseGame(config, 'random')), 'Pulse the leds in random colors'),
    'move': GameSetup((lambda config: MoveGame(config)), 'Move the lines with the controller'),
    'snake': GameSetup((lambda config: SnakeGame(config)), 'Snake game'),
    'snake-two': GameSetup((lambda config: SnakeTwoGame(config)), 'Snake multiplayer game'),
    'tictactoe': GameSetup((lambda config: TicTacToe(config)), 'TicTacToe multiplayer')
}
