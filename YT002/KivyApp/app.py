import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.text import LabelBase
from kivy.graphics import Color, Rectangle
import logging
import requests

# Set up logging
logging.basicConfig(filename='button_presses.log', level=logging.INFO, format='%(asctime)s - %(message)s')

LabelBase.register(name='emoji_font', fn_regular='D:/YT002/KivyApp/emoji.ttf')

class BorderedBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)  # Grey color
            self.border = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, *args):
        self.border.pos = self.pos
        self.border.size = self.size

class MyApp(App):
    def build(self):
        # Main layout container
        main_layout = BoxLayout(orientation='horizontal', padding=20, spacing=10)

        # Create the directional button grid (Section 1)
        direction_layout = GridLayout(cols=3, rows=3, size_hint=(0.2, 1))

        # Add the directional buttons
        direction_layout.add_widget(Button(text='', font_name='emoji_font', background_normal='', background_color=(0, 0, 0, 0)))  # Empty space
        direction_layout.add_widget(Button(text='⬆️', font_name='emoji_font', font_size=24, on_press=lambda x: self.send_request('zoom_in')))
        direction_layout.add_widget(Button(text='', font_name='emoji_font', background_normal='', background_color=(0, 0, 0, 0)))  # Empty space

        direction_layout.add_widget(Button(text='⬅️', font_name='emoji_font', font_size=24, on_press=lambda x: self.send_request('zoom_out')))
        direction_layout.add_widget(Button(text='👓', font_name='emoji_font', font_size=24, on_press=lambda x: self.send_request('zoom_in')))
        direction_layout.add_widget(Button(text='➡️', font_name='emoji_font', font_size=24, on_press=lambda x: self.send_request('zoom_out')))

        direction_layout.add_widget(Button(text='', font_name='emoji_font', background_normal='', background_color=(0, 0, 0, 0)))  # Empty space
        direction_layout.add_widget(Button(text='⬇️', font_name='emoji_font', font_size=24, on_press=lambda x: self.send_request('camera_off')))
        direction_layout.add_widget(Button(text='', font_name='emoji_font', background_normal='', background_color=(0, 0, 0, 0)))  # Empty space

        # Create the button row for other icons (Section 2)
        button_row_layout = GridLayout(cols=2, rows=4, spacing=5, size_hint=(0.1, 1))

        # Add the small buttons
        button_row_layout.add_widget(Button(text='Z-', font_size=24, on_press=lambda x: self.send_request('zoom_out')))
        button_row_layout.add_widget(Button(text='Z+', font_size=24, on_press=lambda x: self.send_request('zoom_in')))
        button_row_layout.add_widget(Button(text='🔋', font_name='emoji_font', font_size=24, on_press=lambda x: self.send_request('battery')))
        button_row_layout.add_widget(Button(text='🔫', font_name='emoji_font', font_size=24, on_press=lambda x: self.send_request('gun')))
        button_row_layout.add_widget(Button(text='🔥', font_name='emoji_font', font_size=24, on_press=lambda x: self.send_request('fire')))
        button_row_layout.add_widget(Button(text='💡', font_name='emoji_font', font_size=24, on_press=lambda x: self.send_request('light')))

        # Create a placeholder for video output with a grey border
        video_output_layout = BorderedBoxLayout(orientation='vertical', size_hint=(0.7, 1), padding=5)
        self.video_output = Image(size_hint=(1, 1))
        video_output_layout.add_widget(self.video_output)

        # Add a button to start video feed
        start_video_button = Button(text='Start Video Feed', size_hint=(0.2, None), height=40)
        start_video_button.bind(on_press=self.start_video_feed)

        # Add layouts to main layout
        main_layout.add_widget(direction_layout)
        main_layout.add_widget(button_row_layout)
        main_layout.add_widget(video_output_layout)  # Video output box next to Section 1
        main_layout.add_widget(start_video_button)  # Button to start video feed

        return main_layout

    def send_request(self, action):
        url = f'http://127.0.0.1:5000/{action}'
        try:
            response = requests.post(url)
            if response.ok:
                print(f'{action} successful')
            else:
                print(f'Failed to {action}')
        except requests.RequestException as e:
            print(f'Error: {e}')

    def start_video_feed(self, instance):
        # Set the source of the video feed and reload
        url = 'http://127.0.0.1:5000/dashboard'
        self.video_output.source = url
        self.video_output.reload()

if __name__ == '__main__':
    MyApp().run()
