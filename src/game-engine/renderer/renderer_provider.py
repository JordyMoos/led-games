from renderer.serial.renderer import SerialRenderer
from renderer.pygame.renderer import PyGameRenderer


class RendererProvider:
    @staticmethod
    def create(config, renderer_name):
        if renderer_name == "PYGAME":
            return PyGameRenderer(config)
        elif renderer_name == "LED":
            return SerialRenderer(config)
        else:
            raise ValueError("Invalid renderer. Valid options are 'PYGAME' and 'LED'")