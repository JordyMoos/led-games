import enum
import pygame


class Buttons(enum.IntEnum):
    left = 1
    up = 2
    right = 3
    down = 4
    ok = 5
    cancel = 6
    start = 7
    select = 8


class ButtonState:
    def __init__(self):
        self.__state = 'not-pressed'
        self.__tick = None

    def press(self, tick):
        if self.__state == 'not-pressed':
            self.__state = 'is-pressed'
            self.__tick = tick

    def release(self):
        if self.__state == 'is-pressed':
            self.__state = 'was-pressed'

    def reset_was_pressed(self):
        if self.__state == 'was-pressed':
            self.__state = 'not-pressed'
            self.__tick = None

    @property
    def get_tick(self):
        return self.__tick

    def is_pressed(self):
        return self.__state == 'is-pressed' or self.__state == 'was-pressed'

    def debug_state(self):
        return self.__state, self.__tick


class InputState:
    direction_keys = [Buttons.left, Buttons.up, Buttons.right, Buttons.down]

    def __init__(self, input_handlers):
        self.__buttons = { key:ButtonState() for key in Buttons }
        self.__input_handlers = input_handlers
        self.__tick = 0

    def handle_event(self, event):
        self.__tick = self.__tick + 1
        [handler.handle_event(self.__tick, event, self.__buttons) for handler in self.__input_handlers]
        # print(self.__buttons[Buttons.left].debug_state())

    def release_buttons(self):
        [button.reset_was_pressed() for button in self.__buttons.values()]

    def get_direction(self):
        pressed_direction_buttons = [(self.__buttons[key].get_tick, key) for key in InputState.direction_keys if self.__buttons[key].is_pressed()]
        pressed_direction_buttons.sort()
        if len(pressed_direction_buttons) > 0:
            first_button, first_key = pressed_direction_buttons[0]
            return first_key

    def is_any_button_pressed(self):
        return any([button.is_pressed() for _, button in self.__buttons.items()])

    def is_pressed(self, button_key):
        return self.__buttons[button_key].is_pressed()


KEY_MAP_1 = {
    pygame.K_a: Buttons.left,
    pygame.K_w: Buttons.up,
    pygame.K_d: Buttons.right,
    pygame.K_s: Buttons.down,
    pygame.K_q: Buttons.ok,
    pygame.K_e: Buttons.cancel,
    pygame.K_z: Buttons.start,
    pygame.K_x: Buttons.select
}

KEY_MAP_2 = {
    pygame.K_j: Buttons.left,
    pygame.K_i: Buttons.up,
    pygame.K_l: Buttons.right,
    pygame.K_k: Buttons.down,
    pygame.K_u: Buttons.ok,
    pygame.K_o: Buttons.cancel,
    pygame.K_m: Buttons.start,
    pygame.K_COMMA: Buttons.select
}


class KeyboardInputHandler:
    def __init__(self, key_map):
        self.__key_map = key_map

    def handle_event(self, tick, event, buttons):
        if event.type == pygame.KEYDOWN:
            self.__handle_keydown(tick, event.key, buttons)
        elif event.type == pygame.KEYUP:
            self.__handle_keyup(tick, event.key, buttons)

    def __handle_keydown(self, tick, key, buttons):
        button_code = self.__key_map.get(key)
        if button_code is not None:
            buttons[button_code].press(tick)

    def __handle_keyup(self, tick, key, buttons):
        button_code = self.__key_map.get(key)
        if button_code is not None:
            buttons[button_code].release()


class JoystickInputHandler:
    def __init__(self, joystick_id):
        self.__joystick_id = joystick_id
        self.__button_map = {
            0: Buttons.ok,
            1: Buttons.cancel,
            9: Buttons.start,
            8: Buttons.select
        }

    def handle_event(self, tick, event, buttons):
        if event.dict.get('joy') != self.__joystick_id:
            return

        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                if event.value < -0.4:
                    buttons.get(Buttons.left).press(tick)
                elif event.value > 0.4:
                    buttons.get(Buttons.right).press(tick)
                else:
                    buttons.get(Buttons.left).release()
                    buttons.get(Buttons.right).release()
            elif event.axis == 1:
                if event.value < -0.4:
                    buttons.get(Buttons.up).press(tick)
                elif event.value > 0.4:
                    buttons.get(Buttons.down).press(tick)
                else:
                    buttons.get(Buttons.up).release()
                    buttons.get(Buttons.down).release()
            if event.axis == 6:
                if event.value < -0.4:
                    buttons.get(Buttons.left).press(tick)
                elif event.value > 0.4:
                    buttons.get(Buttons.right).press(tick)
                else:
                    buttons.get(Buttons.left).release()
                    buttons.get(Buttons.right).release()
            elif event.axis == 7:
                if event.value < -0.4:
                    buttons.get(Buttons.up).press(tick)
                elif event.value > 0.4:
                    buttons.get(Buttons.down).press(tick)
                else:
                    buttons.get(Buttons.up).release()
                    buttons.get(Buttons.down).release()

        elif event.type == pygame.JOYBUTTONDOWN:
            button_code = self.__button_map.get(event.button)
            if button_code is not None:
                buttons[button_code].press(tick)

        elif event.type == pygame.JOYBUTTONUP:
            button_code = self.__button_map.get(event.button)
            if button_code is not None:
                buttons[button_code].release()

        elif event.type == pygame.JOYHATMOTION:
            if event.hat == 0:
                if event.value[0] == -1:
                    buttons[Buttons.left].press(tick)
                elif event.value[0] == 1:
                    buttons[Buttons.right].press(tick)
                else:
                    buttons[Buttons.left].release()
                    buttons[Buttons.right].release()

                if event.value[1] == -1:
                    buttons[Buttons.down].press(tick)
                elif event.value[1] == 1:
                    buttons[Buttons.up].press(tick)
                else:
                    buttons[Buttons.up].release()
                    buttons[Buttons.down].release()


