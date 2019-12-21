
import pyscreenshot as ImageGrab
import numpy as np


class ScreenRecordingGame:
    def __init__(self):
        self.data = []
        self.width = 384
        self.height = 384
        self.x_offset = 8
        self.y_offset = 127
        self.x_pixels_per_cell = self.width / GRID_WIDTH
        self.y_pixels_per_cell = self.height / GRID_HEIGHT

    def update(self, joysticks):
        image = ImageGrab.grab(bbox=(self.x_offset,
                                     self.y_offset,
                                     self.x_offset + self.width,
                                     self.y_offset + self.height))
        self.data = np.asanyarray(image)

    def view(self):
        view = {}

        for x in range(0, GRID_WIDTH):
            x_pixel_position = math.floor(
                (self.x_pixels_per_cell * x) + (self.x_pixels_per_cell / 2))
            for y in range(0, GRID_HEIGHT):
                y_pixel_position = math.floor(
                    (self.y_pixels_per_cell * y) + (self.y_pixels_per_cell / 2))
                color = self.data[y_pixel_position][x_pixel_position]
                view[(x, y)] = color

        return view
