from pygame_widgets.button import Button

from core.car import CarConfig, CA_F, CA_R, MAX_GRIP
from ui.screen import Screen
from ui.widgets.slider import TextSlider


class CarSettingsWidget:

    def __init__(self, car_config: CarConfig, screen):

        self._car_config = car_config

        self.slider_b = TextSlider(screen, y_offset=100, min=0.5, max=5, default=car_config.b, step=0.1, text="center to front (m)", update_lambda=lambda x: self._car_config.set_b(x))
        self.slider_c = TextSlider(screen, y_offset=150, min=0.5, max=5, default=car_config.c, step=0.1, text="center to rear (m)", update_lambda=lambda x: self._car_config.set_c(x))
        self.slider_m = TextSlider(screen, y_offset=200, min=500, max=3000, default=car_config.m, step=1, text="mass (kg)", update_lambda=lambda x: self._car_config.set_m(x))
        self.slider_ca_f = TextSlider(screen, y_offset=250, min=-10, max=0, default=CA_F, step=0.1, text="cornering stiffness front (kN / deg)", update_lambda=lambda x: self._car_config.set_CA_F(x))
        self.slider_ca_r = TextSlider(screen, y_offset=300, min=-10, max=0, default=CA_R, step=0.1, text="cornering stiffness rear (kN / deg)", update_lambda=lambda x: self._car_config.set_CA_R(x))
        self.slider_max_grip = TextSlider(screen, y_offset=350, min=0.5, max=3, default=MAX_GRIP, step=0.1, text="max grip (n)", update_lambda=lambda x: self._car_config.set_MAX_GRIP(x))

        self.sliders = [self.slider_b, self.slider_c, self.slider_m, self.slider_ca_f, self.slider_ca_r, self.slider_max_grip]

        self.reset_button = Button(
            screen, Screen.WIDTH - 80, 50, 70, 30, text='Reset', fontSize=30, margin=20,
            inactiveColour=(200, 200, 200), hoverColour=(150, 150, 150), pressedColour=(100, 100, 100), radius=12,
            onClick=lambda: self.reset()
        )
        self.reset_button.hide()

    def hide(self):
        for slider in self.sliders:
            slider.hide()
        self.reset_button.hide()

    def show(self):
        for slider in self.sliders:
            slider.show()
        self.reset_button.show()

    def update(self):
        for slider in self.sliders:
            slider.update()

    def reset(self):
        for slider in self.sliders:
            slider.reset()


