from kivy.app import App
from kivy.uix.widget import Widget

class MainMenu(Widget):
    pass

class Farm(Widget):
    pass

class DigiApp(App):
    def build(self):
        self.title = 'DigiFarm'
        return MainMenu()


if __name__ == '__main__':
    DigiApp().run()