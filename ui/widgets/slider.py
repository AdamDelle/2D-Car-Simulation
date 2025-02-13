from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

from ui.screen import Screen


class TextSlider:
    def __init__(self, screen, x_offset=600, y_offset=100, width=500, height=10, min=0, max=100, default=0, step=0.1, text="", update_lambda=lambda x: print(x)):
        self._min = min
        self._max = max
        self._default = default
        self._text = text

        # the slider internally only works, if min=0, so we have to adjust the value
        self._slider = Slider(screen, Screen.WIDTH - x_offset, y_offset, width, height, min=0, max=max - min, initial=default - min, step=step, handleRadius=15)
        self._output = TextBox(screen, Screen.WIDTH - x_offset, y_offset, 0, 0, fontSize=30)
        self._update_lambda = update_lambda

        self.hide()

    def show(self):
        self._slider.show()
        self._output.show()

    def hide(self):
        self._slider.hide()
        self._output.hide()

    def set_visibility(self, visible: bool):
        if visible:
            self._slider.show()
            self._output.show()
        else:
            self._slider.hide()
            self._output.hide()

    def get_value(self):
        return self._slider.getValue() + self._min

    def update(self):
        value = round(self.get_value(), 2)
        self._output.setText(self._text + ": " + str(value))
        if self._update_lambda is not None:
            self._update_lambda(value)

    def reset(self):
        self._slider.setValue(self._default - self._min)
        self.update()