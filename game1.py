from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color
from kivy.properties import NumericProperty
from kivy.clock import Clock

class GameWidget(Widget):
    ball_x = NumericProperty(0)
    ball_y = NumericProperty(0)
    ball_velocity_x = NumericProperty(3)
    ball_velocity_y = NumericProperty(4)

    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        self.ball_size = 50
        self.ball_x = self.width / 2
        self.ball_y = self.height / 2
        with self.canvas:
            Color(1, 0, 0, 1)  # Red color
            self.ball = Ellipse(pos=(self.ball_x, self.ball_y), size=(self.ball_size, self.ball_size))
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update(self, dt):
        self.ball_x += self.ball_velocity_x
        self.ball_y += self.ball_velocity_y

        if self.ball_x < 0 or self.ball_x + self.ball_size > self.width:
            self.ball_velocity_x *= -1
        if self.ball_y < 0 or self.ball_y + self.ball_size > self.height:
            self.ball_velocity_y *= -1

        self.ball.pos = (self.ball_x, self.ball_y)

class SimpleGameApp(App):
    def build(self):
        game = GameWidget()
        return game

if __name__ == '__main__':
    SimpleGameApp().run()
