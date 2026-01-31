from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
import random
import string


class ScanLine(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.4, 1, 0.6, 0.8)
            self.rect = RoundedRectangle(size=(self.width, 4), pos=self.pos)
        self.bind(pos=self.update, size=self.update)

    def update(self, *args):
        self.rect.size = (self.width, 4)
        self.rect.pos = self.pos


class ImRichApp(App):
    def build(self):
        self.sound = SoundLoader.load("verify.wav")

        root = FloatLayout()

        with root.canvas.before:
            Color(0.05, 0.07, 0.12, 1)
            self.bg = RoundedRectangle(size=root.size, pos=root.pos)

        root.bind(size=self._update_bg, pos=self._update_bg)

        title = Label(
            text="I AM RICH",
            font_size=64,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(400, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.68},
        )

        self.status = Label(
            text="STATUS UNVERIFIED",
            font_size=18,
            color=(0.7, 0.7, 0.7, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
        )

        self.verify_btn = Button(
            text="VERIFY",
            size_hint=(None, None),
            size=(360, 70),
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            background_normal="",
            background_color=(0.3, 1, 0.6, 1),
            color=(0, 0, 0, 1),
            font_size=20,
        )

        self.verify_btn.bind(on_press=self.start_verification)

        root.add_widget(title)
        root.add_widget(self.status)
        root.add_widget(self.verify_btn)

        return root

    def _update_bg(self, *args):
        self.bg.size = self.root.size
        self.bg.pos = self.root.pos

    def start_verification(self, instance):
        instance.disabled = True
        instance.text = "SCANNING..."

        if self.sound:
            self.sound.play()

        self.status.text = "FACE VERIFICATION IN PROGRESS"

        self.scan = ScanLine(
            size_hint=(1, None),
            height=4,
            pos=(0, self.root.height * 0.25),
        )
        self.root.add_widget(self.scan)

        anim = Animation(y=self.root.height * 0.55, duration=2.5)
        anim.start(self.scan)

        Clock.schedule_once(self.finish_verification, 2.5)

    def finish_verification(self, dt):
        self.root.remove_widget(self.scan)

        fake_id = "XR-" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=12)
        )

        self.status.text = f"STATUS VERIFIED\nID {fake_id}"
        self.status.color = (0.6, 1, 0.7, 1)

        self.verify_btn.text = "VERIFIED"
        self.verify_btn.background_color = (0.2, 0.8, 0.5, 1)

        glow = Animation(opacity=0.6, duration=0.6) + Animation(opacity=1, duration=0.6)
        glow.start(self.verify_btn)


if __name__ == "__main__":
    ImRichApp().run()