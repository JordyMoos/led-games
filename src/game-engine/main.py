
import argparse
import sys
from games.games import games
import defaults
from config.pair_config import PairConfig
from config.led_config import LedConfig
from config.config import Config
from engine.game_engine import GameEngine


class Main:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Led the light show begin!',
            usage='''python3 ./main.py <command> [<args>]

The most commonly used commands are:
   list       List all the games
   run        Run a game
''')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    @staticmethod
    def list():
        parser = argparse.ArgumentParser(
            description='List all games')
        args = parser.parse_args(sys.argv[2:])
        print(games.keys())

    @staticmethod
    def run():
        parser = argparse.ArgumentParser(
            description='Run a game')
        parser.add_argument('game')
        parser.add_argument('--renderer',
                            choices=['LED', 'PYGAME'],
                            default=defaults.DEFAULT_RENDERER,
                            help='Use LED to control phisical leds. Use PYGAME for testing. Default: %s' % defaults.DEFAULT_RENDERER)
        parser.add_argument('--total-leds',
                            default=defaults.DEFAULT_TOTAL_LEDS,
                            help='The total number of leds. This must match the configuration on the Teensy. Default: %s' % defaults.DEFAULT_TOTAL_LEDS)
        parser.add_argument('--max-leds',
                            default=defaults.DEFAULT_MAX_LEDS_PER_CELL,
                            help='Max leds per cell (That is an X,Y coordinate in the game), this is handy to reduce bright clusters. Default: %s' % defaults.DEFAULT_MAX_LEDS_PER_CELL)
        parser.add_argument('--max-brightness',
                            default=defaults.DEFAULT_MAX_BRIGHTNESS,
                            help='Possible values between 0 and 255. Scales the brightness of the leds. The leds can be really bright and with this value you can scale that down. Default: %s' % defaults.DEFAULT_MAX_BRIGHTNESS)
        parser.add_argument('--pair-file',
                            default=defaults.DEFAULT_PAIRING_FILE,
                            help='The pair file which holds the led numbers and their positions. This is created by `src/tools/02-process-photos/process.py`. Default: %s' % defaults.DEFAULT_PAIRING_FILE)
        parser.add_argument('--view-files',
                            nargs='+',
                            default=defaults.DEFAULT_VIEW_FILES,
                            help='One or more view files. One view file is created by `src/tools/02-process-photos/process.py`. Default: %s' % defaults.DEFAULT_VIEW_FILES)
        parser.add_argument('--min-x',
                            default=defaults.DEFAULT_PAIRING_MIN_X,
                            help='This helps cropping the screen. Default: %s' % defaults.DEFAULT_PAIRING_MIN_X)
        parser.add_argument('--max-x',
                            default=defaults.DEFAULT_PAIRING_MAX_X,
                            help='This helps cropping the screen. Default: %s' % defaults.DEFAULT_PAIRING_MAX_X)
        parser.add_argument('--min-y',
                            default=defaults.DEFAULT_PAIRING_MIN_Y,
                            help='This helps cropping the screen. Default: %s' % defaults.DEFAULT_PAIRING_MIN_Y)
        parser.add_argument('--max-y',
                            default=defaults.DEFAULT_PAIRING_MAX_Y,
                            help='This helps cropping the screen. Default: %s' % defaults.DEFAULT_PAIRING_MAX_Y)
        parser.add_argument('--grid-width',
                            default=defaults.DEFAULT_GRID_WIDTH,
                            help='The width of the game screen. Default: %s' % defaults.DEFAULT_GRID_WIDTH)
        parser.add_argument('--grid-height',
                            default=defaults.DEFAULT_GRID_HEIGHT,
                            help='The height of the game screen. Default: %s' % defaults.DEFAULT_GRID_HEIGHT)
        parser.add_argument('--serial-port',
                            default=defaults.DEFAULT_SERIAL_PORT,
                            help='The serial port towards the Teensy. This is only used if `--renderer` is `LED. Default: %s' % defaults.DEFAULT_SERIAL_PORT)
        parser.add_argument('--fps',
                            default=defaults.DEFAULT_FPS,
                            help='How fast the game runs. Default: %s' % defaults.DEFAULT_FPS)

        args = parser.parse_args(sys.argv[2:])
        game_setup = games[args.game]
        led_config = LedConfig(
            total=int(args.total_leds),
            per_cell=int(args.max_leds),
            max_brightness=int(args.max_brightness)
        )
        pair_config = PairConfig(
            pair_file=args.pair_file,
            view_files=args.view_files,
            min_x=int(args.min_x),
            max_x=int(args.max_x),
            min_y=int(args.min_y),
            max_y=int(args.max_y),
            grid_width=int(args.grid_width),
            grid_height=int(args.grid_height)
        )
        config = Config(
            led=led_config,
            pair=pair_config,
            serial_port=args.serial_port,
            fps=int(args.fps)
        )
        game = game_setup.create(config)

        engine = GameEngine(args.renderer, config, game)
        engine.start()


if __name__ == '__main__':
    Main()
