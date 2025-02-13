from pygame_widgets.button import Button
from core.car import CarConfig
from ui.screen import Screen
from ui.widgets.slider import TextSlider
from pygame_widgets.toggle import Toggle
from pygame_widgets.textbox import TextBox
from ui.screen import Screen


class CarSettingsWidget:

    def __init__(self, car_config: CarConfig, screen):

        self._car_config = car_config

        current_y = 50
        current_x = Screen.WIDTH -600
        increment_y = 70
        self.mode_toggle = Toggle(screen, current_x, current_y, 20, 20)
        self.mode_toggle_label = TextBox(screen, current_x + 30, current_y+35, 0, 0, fontSize=30)
        self.mode_toggle_label.setText("Debug Mode")

        current_y += increment_y
        self.show_hide_toggle = Toggle(screen, current_x, current_y, 20, 20)
        self.show_hide_toggle_label = TextBox(screen, current_x + 30, current_y+35, 0, 0, fontSize=30)
        self.show_hide_toggle_label.setText("Settings")

        current_y += increment_y
        self.slider_b = TextSlider(screen, y_offset=current_y, min=0.5, max=5, default=car_config.b, step=0.1, text="center to front (m)", update_lambda=lambda x: self._car_config.set_b(x))
        current_y += increment_y
        self.slider_c = TextSlider(screen, y_offset=current_y, min=0.5, max=5, default=car_config.c, step=0.1, text="center to rear (m)", update_lambda=lambda x: self._car_config.set_c(x))
        current_y += increment_y
        self.slider_m = TextSlider(screen, y_offset=current_y, min=500, max=3000, default=car_config.m, step=1, text="mass (kg)", update_lambda=lambda x: self._car_config.set_m(x))
        current_y += increment_y
        self.slider_ca_f = TextSlider(screen, y_offset=current_y, min=-10, max=0, default=car_config.cornering_front, step=0.1, text="cornering stiffness front (kN / deg)", update_lambda=lambda x: self._car_config.set_cornering_front(x))
        current_y += increment_y
        self.slider_ca_r = TextSlider(screen, y_offset=current_y, min=-10, max=0, default=car_config.cornering_rear, step=0.1, text="cornering stiffness rear (kN / deg)", update_lambda=lambda x: self._car_config.set_cornering_rear(x))
        current_y += increment_y
        self.slider_max_grip = TextSlider(screen, y_offset=current_y, min=0.5, max=3, default=car_config.max_grip, step=0.1, text="max grip (n)", update_lambda=lambda x: self._car_config.set_max_grip(x))

        current_y += increment_y
        self.acceleration_toggle = Toggle(screen, current_x, current_y, 20, 20)
        self.acceleration_toggle_label = TextBox(screen, current_x + 30, current_y+35, 0, 0, fontSize=30)
        self.acceleration_toggle_label.setText("Show Acc Vector")

        current_y += increment_y
        self.resistance_toggle = Toggle(screen, current_x, current_y, 20, 20)
        self.resistance_toggle_label = TextBox(screen, current_x + 30, current_y+35, 0, 0, fontSize=30)
        self.resistance_toggle_label.setText("Show Res Vector")

        current_y += increment_y
        self.velocity_toggle = Toggle(screen, current_x, current_y, 20, 20)
        self.velocity_toggle_label = TextBox(screen, current_x + 30, current_y+35, 0, 0, fontSize=30)
        self.velocity_toggle_label.setText("Show Vel Vector")

        current_y += increment_y
        self.friction_circle_toggle = Toggle(screen, current_x, current_y, 20, 20)
        self.friction_circle_toggle_label = TextBox(screen, current_x + 30, current_y+35, 0, 0, fontSize=30)
        self.friction_circle_toggle_label.setText("Show Friciton Circle")

        current_y += increment_y
        self.reset_button = Button(
            screen, current_x, current_y, 80, 40, text='Reset', fontSize=30, margin=20,
            inactiveColour=(200, 200, 200), hoverColour=(150, 150, 150), pressedColour=(100, 100, 100), radius=12,
            onClick=lambda: self.reset()
        )
        self.reset_button.hide()

        self.sliders = [self.slider_b, self.slider_c, self.slider_m, self.slider_ca_f, self.slider_ca_r, self.slider_max_grip]

    def hide(self):
        for slider in self.sliders:
            slider.hide()
        self.reset_button.hide()
        self.velocity_toggle.hide()
        self.velocity_toggle_label.hide()
        self.acceleration_toggle.hide()
        self.acceleration_toggle_label.hide()
        self.friction_circle_toggle.hide()
        self.friction_circle_toggle_label.hide()
        self.resistance_toggle.hide()
        self.resistance_toggle_label.hide()

    def show(self):
        for slider in self.sliders:
            slider.show()
        self.reset_button.show()
        self.reset_button.show()
        self.velocity_toggle.show()
        self.velocity_toggle_label.show()
        self.acceleration_toggle.show()
        self.acceleration_toggle_label.show()
        self.friction_circle_toggle.show()
        self.friction_circle_toggle_label.show()
        self.resistance_toggle.show()
        self.resistance_toggle_label.show()

    def update(self):
        for slider in self.sliders:
            slider.update()
        if self.show_hide_toggle.value:
            self.show()
        else:
            self.hide()

    def reset(self):
        for slider in self.sliders:
            slider.reset()

    def draw(self):
        self.mode_toggle.draw()
        self.mode_toggle_label.draw()
        self.show_hide_toggle.draw()
        self.show_hide_toggle_label.draw()
        self.velocity_toggle.draw()
        self.velocity_toggle_label.draw()
        self.acceleration_toggle.draw()
        self.acceleration_toggle_label.draw()
        self.friction_circle_toggle.draw()
        self.friction_circle_toggle_label.draw()
        self.resistance_toggle.draw()
        self.resistance_toggle_label.draw()
        for slider in self.sliders:
            slider._slider.draw()
            slider._output.draw()
        self.reset_button.draw()


