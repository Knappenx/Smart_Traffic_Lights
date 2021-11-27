
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.videoplayer import VideoPlayer
from kivy.lang import Builder

Builder.load_file('styles/main.kv')

class WindowLayout(Widget):
    """Main application layout"""
    pass

class MainApp(App):
    def build(self):
        # start playing the video at creation
        #video = VideoPlayer(source='./car_detector/contituyentes_demo.mp4', state='play')

        # create the video, and start later
        #source = './car_detector/contituyentes_demo.mp4'
        #video = VideoPlayer(source=source)
        # and later
        #video.state = 'play'
        return WindowLayout()
MainApp().run()