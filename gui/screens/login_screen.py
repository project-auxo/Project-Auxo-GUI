"""
Provides the login and authentication
"""

from kivy.app import App
from kivy.uix.screenmanager import SlideTransition, Screen


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

    def _show_toast(self, text):
        self.ids['toast'].show(text)

    def on_enter(self):
        self.ids['username'].focus = True   # so the user can begin typing right away

    def do_login(self, username, password):
        # Make sure to perform the authentication
        app = App.get_running_app()

        app.username = username
        app.password = password

        self.verify__credentials(app.username, app.password)

    def login_failure(self, error):
        self._show_toast(error)

    def verify__credentials(self, username, password):
        if username != 'admin' or password != 'admin':
            self.login_failure('invalid credentials')
        else:
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'connected_screen'

        self.reset_forms()

    def reset_forms(self):
        self.ids['password'].text = ""

    def move_next(self):
        self.ids['username'].focus = False