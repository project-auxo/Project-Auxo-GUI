import os
import glob

from kivy.config import Config
Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '800')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, DictProperty
from kivy.uix.screenmanager import ScreenManager

import gui.screens as screens

# MARK: TODOs
# TODO: Implement a way to dynamically load a scrolling view of the BBBs (Kivy Recycleview?)
# TODO: Implement the service to connect to the agent via ssh (naw, do so via the REST endpoints) -- fix screen as well
# TODO: Make the application faster!

# MARK: Config and load appropriate kv file
relevant_dirs = ('kv')
dirname = os.path.dirname(__file__) + "/kv/**"
for kv_file in glob.glob(os.path.join(dirname, "*.kv"), recursive=True):
    Builder.load_file(kv_file)


class ProjectAuxoApp(App):
    icon = 'assets/Auxo_Logo_Black.png'
    title = 'Auxo Olympus'

    username = StringProperty("")
    password = StringProperty("")
    agent_name = StringProperty("")

    alive_agents = DictProperty(None)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(screens.login_screen.LoginScreen(name='login_screen'))
        manager.add_widget(screens.connected_screen.ConnectedScreen(name='connected_screen'))
        manager.add_widget(screens.agent_screen.AgentScreen(name='agent_screen'))

        return manager


if __name__ == '__main__':
    ProjectAuxoApp().run()
