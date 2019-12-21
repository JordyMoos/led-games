import serial
import os
import pygame


class SerialRenderer:
    def __init__(self, config):
        self.__serial_port = config.serial_port
        self.__total_leds = config.led.total

        self.__serial = serial.Serial(
            port=self.__serial_port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.display.set_mode((1, 1))

    def render(self, screen):
        self.__serial.write(bytes(
            list('*'.encode()) +
            list(self.__total_leds.to_bytes(2, byteorder='big')) +
            screen.physical_leds))
