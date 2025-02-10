from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

from UI.screen import Screen


class TextSlider:
    def __init__(self, screen, x_offset=600, y_offset=100, width=500, height=10, min=0, max=100, step=0.1, text=""):
        self._text = text
        self._slider = Slider(screen, Screen.WIDTH - x_offset, y_offset, width, height, min=min, max=max, step=step, handleRadius=15)

        self._output = TextBox(screen, Screen.WIDTH - x_offset, y_offset, 0, 0, fontSize=30)
        self._output.disable()
        self.set_visibility(False)

    def set_visibility(self, visible: bool):
        if visible:
            self._slider.show()
            self._output.show()
        else:
            self._slider.hide()
            self._output.hide()

    def get_value(self):
        return self._slider.getValue()

    def update(self):
        value = str(round(self._slider.getValue(), 2))
        self._output.setText(self._text + ": " + value)