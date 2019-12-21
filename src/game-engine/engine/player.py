
class Player:
    def __init__(self, input_state):
        self.__input = input_state

    @property
    def input(self):
        return self.__input
