from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder

Builder.load_file('styles/main.kv')

class WindowLayout(Widget):
    """Main application layout"""
    pass

class MainApp(App):
    def build(self):
        return WindowLayout()
MainApp().run()