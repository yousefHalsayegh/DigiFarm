from kivy.app import App
from kivy.uix.widget import Widget

class MainMenu(Widget):
    pass

class DigiApp(App):
    def build(self):
        return MainMenu()


if __name__ == '__main__':
    DigiApp().run()