"""
Provides the login and authentication
"""

from kivy.app import App
from kivy.uix.screenmanager import SlideTransition, Screen
from kivy.uix.boxlayout import BoxLayout


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.register_event_type('on_login')

    def try_login(self):
        if self.ids['grid'].username is '':
            self.login_failure('username is empty')
        elif self.ids['grid'].password is '':
            self.login_failure('password is empty')
        else:
            self.dispatch('on_login')

    def login_failure(self, error):
        print(error)        # will be replaced with toast

    def on_login(self):
        pass


class LoginGrid(BoxLayout):
    username = ''
    password = ''

    def __init__(self, **kwargs):
        super(LoginGrid, self).__init__(**kwargs)
        self.register_event_type('on_login')

    def on_password(self, value):
        self.password = value

    def on_username(self, value):
        self.username = value

    # def on_disabled(self, instance, disabled):
    #     super().on_disabled(instance, disabled)
    #     if not disabled:
    #         self.ids['input_username'].hint_text = 'username'
    #         self.ids['input_password'].hint_text = 'password'

    def on_login(self):
        pass

# class LoginScreen(Screen):
#
#     def on_enter(self):
#         self.ids['username'].focus = True   # so the user can begin typing right away
#
#     def do_login(self, username, password):
#         # Make sure to perform the authentication
#         app = App.get_running_app()
#
#         app.username = username
#         app.password = password
#
#         self.verify__credentials(app.username, app.password)
#
#     def verify__credentials(self, username, password):
#         if username != 'admin' or password != 'admin':
#             print('Invalid Credentials. Please try again.')
#         else:
#             self.manager.transition = SlideTransition(direction='up')
#             self.manager.current = 'connected_screen'
#
#         self.reset_forms()
#
#     def reset_forms(self):
#         self.ids['password'].text = ""
#
#     def move_next(self):
#         self.ids['username'].focus = False
