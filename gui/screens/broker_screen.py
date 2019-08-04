"""
Screen when connected to the broker
"""

from kivy.uix.screenmanager import SlideTransition, Screen


class BrokerScreen(Screen):

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'connected_screen'
