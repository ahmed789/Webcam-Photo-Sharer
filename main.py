from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import ClipboardBase, Clipboard
import time
import webbrowser
from filesharer import FileSharer

Builder.load_file('frontend.kv')


class CameraScreen(Screen):
    filepath = None

    def start(self):
        """start the camera and change the button text"""
        self.ids.camera.opacity = 1
        self.ids.camera.play = True
        self.ids.camera_button.text = 'Stop camera'
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        """stop the camera and change the button text"""
        self.ids.camera.opacity = 0
        self.ids.camera.play = False
        self.ids.camera_button.text = 'Start camera'
        self.ids.camera.texture = None

    def capture(self):
        """create an image from camera and save it in the time which taken at"""
        current_time = time.strftime('%Y_%m_%d--%H_%M_%S')
        self.filepath = f"files/{current_time} .png"
        self.ids.camera.export_to_png(self.filepath)
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.img.source = self.filepath


class ImageScreen(Screen):
    file_path = None
    url = None
    new_url = ''
    warning_message = 'Create a Link First'

    def create_link(self):
        """create a link of the image taken"""
        self.file_path = App.get_running_app().root.ids.camera_screen.filepath
        filesharer = FileSharer(filepath=self.file_path)
        self.url = filesharer.share()
        new_url = str(self.url)
        new_url = new_url[9:]
        new_url = f'https://cdn.filestackcontent.com/{new_url[:-1]}'
        self.ids.link.text = str(new_url).strip()

    def copy_link(self):
        """copy the link of image to clapboard"""
        self.new_url = str(self.url)
        self.new_url = self.new_url[9:]
        self.new_url = f'https://cdn.filestackcontent.com/{self.new_url[:-1]}'.strip()
        try:
            Clipboard.copy(self.new_url)
        except:
            self.ids.link.text = self.warning_message

    def open_link(self):
        webbrowser.open(self.new_url)


class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()


MainApp().run()
