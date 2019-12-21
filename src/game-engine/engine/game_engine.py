import pygame

import engine.input as ei
from engine.input import InputState, KeyboardInputHandler, JoystickInputHandler
from engine.player import Player
from engine.screen import ScreenProvider
from renderer.renderer_provider import RendererProvider


class GameEngine:
    def __init__(self, renderer_name, config, game):
        self.__config = config
        self.__game = game

        pygame.init()
        self.__clock = pygame.time.Clock()

        self.__screen = ScreenProvider.create(config)
        self.__renderer = RendererProvider.create(config, renderer_name)
        self.__done = False
        self.__joysticks = []

        self.__connect_joysticks()

        self.__players = [
            Player(InputState([KeyboardInputHandler(ei.KEY_MAP_1), JoystickInputHandler(0)])),
            Player(InputState([KeyboardInputHandler(ei.KEY_MAP_2), JoystickInputHandler(1)]))
        ]

    def start(self):
        while not self.__done:
            self.__handle_events()
            self.__tick()
            self.__handle_release_buttons()
            self.__clock.tick(self.__config.fps)

    def __connect_joysticks(self):
        pygame.joystick.init()
        self.__joysticks = [pygame.joystick.Joystick(id) for id in range(pygame.joystick.get_count())]
        [joystick.init() for joystick in self.__joysticks]

    def __handle_events(self):
        for event in pygame.event.get():
            #print((pygame.event.event_name(event.type), event.type, event))
            if event.type == pygame.QUIT:
                self.__done = True
            elif event.type == 1541:
                # Device connected
                self.__connect_joysticks()
            elif event.type == 1542:
                # Device lost
                self.__connect_joysticks()

            for player in self.__players:
                player.input.handle_event(event)

    def __tick(self):
        self.__game.update(self.__players)

        self.__screen.clear()
        self.__game.view(self.__screen)
        self.__renderer.render(self.__screen)

    def __handle_release_buttons(self):
        for player in self.__players:
            player.input.release_buttons()
