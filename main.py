from kivy.app import App
from kivy.uix.widget import Widget 

class DigiFarm(Widget):
    pass


class DigiApp(App):
    def build(self):
        return DigiFarm()


if __name__ == '__main__':
    DigiApp().run()