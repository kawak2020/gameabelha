from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ListProperty
from kivy.graphics import Rectangle, Color, Rotate
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.image import Image as CoreImage
from random import randint
from math import atan2, degrees

class Pollen(Widget):
    def __init__(self, pos, size, **kwargs):
        super(Pollen, self).__init__(**kwargs)
        with self.canvas:
            self.texture = CoreImage('polen_sprite.png').texture
            self.rect = Rectangle(texture=self.texture, pos=pos, size=size)

    def remove(self):
        self.canvas.clear()

class Flower(Widget):
    pollen_count = NumericProperty(3)
    pollen_list = ListProperty([])

    def __init__(self, pos, size, **kwargs):
        super(Flower, self).__init__(**kwargs)
        self.size = size
        self.pos = pos
        with self.canvas:
            self.texture = CoreImage('flor_sprite.png').texture
            self.rect = Rectangle(texture=self.texture, pos=pos, size=size)

        self.create_pollen()

    def create_pollen(self):
        for _ in range(self.pollen_count):
            pollen_x = self.x + randint(0, self.width - 20)
            pollen_y = self.y + randint(0, self.height - 20)
            pollen = Pollen(pos=(pollen_x, pollen_y), size=(20, 20))
            self.pollen_list.append(pollen)
            self.add_widget(pollen)

    def collect_pollen(self):
        collected = len(self.pollen_list)
        for pollen in self.pollen_list:
            pollen.remove()
        self.pollen_list = []
        return collected

class GameWidget(Widget):
    abelha_x = NumericProperty(100)
    abelha_y = NumericProperty(100)
    pontos = NumericProperty(0)
    flores = ListProperty([])
    total_pollen = NumericProperty(0)
    rotation = Rotate(angle=0, origin=(0, 0))

    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        self.abelha_size = 50
        self.velocidade = 5

        with self.canvas:
            # Desenhar fundo branco para garantir visibilidade do texto
            self.canvas.before.add(Color(1, 1, 1, 1))
            self.canvas.before.add(Rectangle(size=Window.size))

            try:
                self.abelha_image = CoreImage('abelha_sprite.png').texture
                self.rotation = Rotate(angle=0, origin=(self.abelha_x + self.abelha_size / 2, self.abelha_y + self.abelha_size / 2))
                self.canvas.before.add(self.rotation)
                self.abelha = Rectangle(texture=self.abelha_image, pos=(self.abelha_x, self.abelha_y), size=(self.abelha_size, self.abelha_size))
            except Exception as e:
                print(f"Erro ao carregar a imagem da abelha: {e}")

        # Barra de status
        self.status_bar = BoxLayout(size_hint=(1, None), height=50)
        self.label = Label(text="Pontos: 0", font_size='20sp', color=(0, 0, 0, 1))  # Letras pretas
        self.status_bar.add_widget(self.label)
        self.add_widget(self.status_bar)

        self.bind(pontos=self.update_pontos)
        self.create_flowers()

        Window.bind(on_key_down=self.on_key_down)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def create_flowers(self):
        for _ in range(10):
            flor_x = randint(0, self.width - 100)
            flor_y = randint(0, self.height - 100)
            flower = Flower(pos=(flor_x, flor_y), size=(70, 70))
            self.flores.append(flower)
            self.add_widget(flower)
            self.total_pollen += flower.pollen_count

    def on_key_down(self, window, key, *args):
        if key == 273:  # Seta para cima
            self.abelha_y += self.velocidade
        elif key == 274:  # Seta para baixo
            self.abelha_y -= self.velocidade
        elif key == 275:  # Seta para a direita
            self.abelha_x += self.velocidade
        elif key == 276:  # Seta para a esquerda
            self.abelha_x -= self.velocidade
        self.abelha.pos = (self.abelha_x, self.abelha_y)

    def update(self, dt):
        # Verifica se a abelha tocou alguma flor
        for flower in self.flores:
            if self.collide_widget(self.abelha, flower):
                collected = flower.collect_pollen()
                self.pontos += collected

        if self.pontos >= self.total_pollen:
            self.show_congratulations()

    def rotate_to_target(self):
        angle = atan2(self.target_y - self.abelha_y, self.target_x - self.abelha_x)
        self.rotation.angle = degrees(angle) - 90  # Ajustar para que a abelha fique na direção do movimento

    def collide_widget(self, widget1, widget2):
        widget1_x, widget1_y = widget1.pos
        widget2_x, widget2_y = widget2.pos
        return (widget1_x < widget2_x + widget2.size[0] and
                widget1_x + widget1.size[0] > widget2_x and
                widget1_y < widget2_y + widget2.size[1] and
                widget1_y + widget1.size[1] > widget2_y)

    def update_pontos(self, instance, value):
        self.label.text = f"Pontos: {value}"

    def show_congratulations(self):
        self.clear_widgets()
        congrats_label = Label(text=f"Parabéns! Você recolheu {self.pontos} polens.", font_size='20sp', color=(0, 0, 0, 1), pos=(Window.width / 2 - 150, Window.height / 2))
        self.add_widget(congrats_label)

        restart_button = Button(text='Recomeçar', size_hint=(None, None), size=(200, 50), pos=(Window.width / 2 - 100, Window.height / 2 - 50))
        restart_button.bind(on_release=self.restart_game)
        self.add_widget(restart_button)

    def restart_game(self, instance):
        self.clear_widgets()
        self.__init__()

class AbelhaApp(App):
    def build(self):
        return GameWidget()

if __name__ == '__main__':
    AbelhaApp().run()
