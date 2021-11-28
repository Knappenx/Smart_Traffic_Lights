
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.videoplayer import VideoPlayer
from kivy.lang import Builder
from car_detector.main import CarDetector

Builder.load_file('styles/main.kv')

class WindowLayout(Widget):
    """Main application layout"""
    pass

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.car_detector = CarDetector(VideoPlayer)

    def build(self):
        self.car_detector.start()
        #start playing the video at creation
        ##video = VideoPlayer(source='./contituyentes_demo.mp4', state='play')
        ##return video
        # create the video, and start later
        #source = './car_detector/contituyentes_demo.mp4'
        #video = VideoPlayer(source=source)
        # and later
        #video.state = 'play'
        return WindowLayout()
MainApp().run()