
class Config:
    def __init__(self, led, pair, serial_port, fps):
        self.__led = led
        self.__pair = pair
        self.__serial_port = serial_port
        self.__fps = fps

    @property
    def led(self):
        return self.__led

    @property
    def pair(self):
        return self.__pair

    @property
    def serial_port(self):
        return self.__serial_port

    @property
    def fps(self):
        return self.__fps