from UI.ui_widgets.slider import TextSlider
from car import CarConfig


class CarSettingsWidget:

    def __init__(self, car_config: CarConfig, screen):
        self._car_config = car_config

        self.slider_length = TextSlider(screen, y_offset=100, min=2, max=5, step=0.1, text="length (m)")
        self.slider_m = TextSlider(screen, y_offset=150, min=500, max=3000, step=1, text="mass (kg)")

    def set_visibility(self, visible: bool):
        self.slider_length.set_visibility(visible)
        self.slider_m.set_visibility(visible)

    def update(self):
        self.slider_length.update()
        #self._car_config.length = self.slider_length.get_value()
        self.slider_m.update()
        #self._car_config.c = self.slider_m.get_value()



