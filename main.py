from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from filesharer import FileSharer
import webbrowser
import time

Builder.load_file('frontend.kv')

class CameraScreen(Screen):
    def start(self):
        self.ids.camera.opacity = 1
        self.ids.camera.play = True
        self.ids.camera_button.text = 'Stop Camera'
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        self.ids.camera.opacity = 0
        self.ids.camera.play = False
        self.ids.camera_button.text = 'Start Camera'
        self.ids.camera.texture = None


    def capture(self):
        if self.ids.camera.opacity == 1:
            current_time = time.strftime('%Y%m%d-%H%M%S')
            self.filepath = f'files/{current_time}.png'
            self.ids.camera.export_to_png(self.filepath)
            self.manager.current = 'image_screen'
            self.manager.current_screen.ids.img.source = self.filepath
        else:
            self.ids.notice.text = 'Start the camera first'
            



class ImageScreen(Screen):
    def create_link(self):
        file_path = App.get_running_app().root.ids.camera_screen.filepath
        fileshare = FileSharer(filepath=file_path)
        self.url = fileshare.share()
        self.ids.link.text = self.url

    def copy_link(self):
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = 'Create link first'

    def open_link(self):
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = 'Create a link first'


class RootWidget(ScreenManager):
    pass

class MainApp(App):

    def build(self):
        return RootWidget()

MainApp().run()