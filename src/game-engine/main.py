
import argparse
import sys
from games.presets import game_presets
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
   list       List all the presets
   run        Run a preset
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
            description='List all presets')
        args = parser.parse_args(sys.argv[2:])
        print(game_presets.keys())

    @staticmethod
    def run():
        parser = argparse.ArgumentParser(
            description='Run a preset')
        parser.add_argument('preset')
        parser.add_argument('--renderer', choices=['LED', 'PYGAME'], default=defaults.DEFAULT_RENDERER)
        parser.add_argument('--total-leds', default=defaults.DEFAULT_TOTAL_LEDS)
        parser.add_argument('--max-leds', default=defaults.DEFAULT_MAX_LEDS_PER_CELL)
        parser.add_argument('--max-brightness', default=defaults.DEFAULT_MAX_BRIGHTNESS)
        parser.add_argument('--pair-file', default=defaults.DEFAULT_PAIRING_FILE)
        parser.add_argument('--view-files', nargs='+', default=defaults.DEFAULT_VIEW_FILES)
        parser.add_argument('--min-x', default=defaults.DEFAULT_PAIRING_MIN_X)
        parser.add_argument('--max-x', default=defaults.DEFAULT_PAIRING_MAX_X)
        parser.add_argument('--min-y', default=defaults.DEFAULT_PAIRING_MIN_Y)
        parser.add_argument('--max-y', default=defaults.DEFAULT_PAIRING_MAX_Y)
        parser.add_argument('--grid-width', default=defaults.DEFAULT_GRID_WIDTH)
        parser.add_argument('--grid-height', default=defaults.DEFAULT_GRID_HEIGHT)
        parser.add_argument('--serial-port', default=defaults.DEFAULT_SERIAL_PORT)
        parser.add_argument('--fps', default=defaults.DEFAULT_FPS)

        args = parser.parse_args(sys.argv[2:])
        preset = game_presets[args.preset]
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
        game = preset.create(config)

        engine = GameEngine(args.renderer, config, game)
        engine.start()


if __name__ == '__main__':
    Main()
