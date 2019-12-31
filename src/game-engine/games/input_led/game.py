class InputLedGame:
    def __init__(self, config):
        self.__total = config.led.total
        self.__led_index = 0

    def update(self, players):
        led_index = int(input("Index:"))
        if led_index < 0 or led_index >= self.__total:
            print("Index is out of bound")
            return

        self.__led_index = led_index

    def view(self, screen):
        screen.set_led_color(self.__led_index, 100, 0, 20)

