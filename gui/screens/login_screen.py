"""
Provides the login and authentication
"""

from kivy.app import App
from kivy.uix.screenmanager import SlideTransition, Screen


class LoginScreen(Screen):

    def on_enter(self):
        self.ids['username'].focus = True   # so the user can begin typing right away

    def do_login(self, username, password):
        # Make sure to perform the authentication
        app = App.get_running_app()

        app.username = username
        app.password = password

        self.verify__credentials(app.username, app.password)

    def verify__credentials(self, username, password):
        if username != 'admin' or password != 'admin':
            print('Invalid Credentials. Please try again.')
        else:
            self.manager.transition = SlideTransition(direction='up')
            self.manager.current = 'connected_screen'

        self.reset_forms()

    def reset_forms(self):
        self.ids['password'].text = ""

    def move_next(self):
        self.ids['username'].focus = False