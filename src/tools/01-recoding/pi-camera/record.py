
import os
import time
import serial
from picamera import PiCamera

# the serial port towards the Teensy for example '/dev/ttyACM0'
SERIAL_PORT = '/dev/ttyACM0'

# total leds
# must match the Arduino
TOTAL_LEDS = 800

# create a background image every x leds
# handy if light of the room changes over time
BACKGROUND_INTERVAL = 10

# folder to store the images
STORE_STRATEGY_DIR = './photos-' + str(round(time.time()))

# the led index where you would like to start the recording from
STARTING_LED_INDEX = 0

# the color of the led in (RED, GREEN, BLUE) where all values must be between 0 and 255
# where the higher the color value, the brighter the led is
# having to dimmed leds might make it too difficult for the camera to spot the led
# but too bright leds might illumine too much on the environment
# for example:
# COLOR = (255, 0, 0) # bright red
# COLOR = (0, 255, 0) # bright green
# COLOR = (0, 0, 255) # bright blue
COLOR = (100, 0, 0)   # not too bright red

'''

    End of configuration
    
'''

if not os.path.exists(STORE_STRATEGY_DIR):
    os.makedirs(STORE_STRATEGY_DIR)


class Record:
    def __init__(self, starting_led_index, total_leds, background_interval):
        self.leds = []
        self.starting_led_index = starting_led_index
        self.background_interval = background_interval
        self.total_leds = total_leds

        self.ser = serial.Serial(
           port=SERIAL_PORT,
           baudrate=9600,
           parity=serial.PARITY_NONE,
           stopbits=serial.STOPBITS_ONE,
           bytesize=serial.EIGHTBITS,
           timeout=1
        )
        self.clear_leds()

        # setting up the camera
        self.cam = PiCamera()
        self.cam.resolution = (1920, 1080)
        self.cam.start_preview()
        # sleep to give the camera time to adjust
        time.sleep(3)

    def record(self):
        for led_index in range(self.starting_led_index, self.total_leds):
            if led_index == self.starting_led_index or (led_index % self.background_interval) == 0:
                self.create_background(led_index)

            self.record_led(led_index)

    def create_background(self, led_index):
        print("Creating background")
        self.clear_leds()
        time.sleep(0.1)
        self.cam.capture("%s/%05d-background.jpg" % (STORE_STRATEGY_DIR, led_index))

    def record_led(self, led_index):
        print("Recording led %d" % led_index)
        self.clear_leds()
        self.turn_on_current_led(led_index)
        time.sleep(0.1)
        self.cam.capture("%s/%05d-led.jpg" % (STORE_STRATEGY_DIR, led_index))

    def clear_leds(self):
        self.leds = [0, 0, 0] * TOTAL_LEDS
        self.render_leds()

    def turn_on_current_led(self, led_index):
        key = led_index * 3
        self.leds[key] = COLOR[0]
        self.leds[key + 1] = COLOR[1]
        self.leds[key + 2] = COLOR[2]
        self.render_leds()

    def render_leds(self):
        self.ser.write(bytes(
            list('*'.encode()) +
            list(TOTAL_LEDS.to_bytes(2, byteorder='big')) + self.leds))


record = Record(STARTING_LED_INDEX, TOTAL_LEDS, BACKGROUND_INTERVAL)
record.record()
