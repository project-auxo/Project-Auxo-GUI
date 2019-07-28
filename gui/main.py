from kivy.config import Config
Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '800')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, DictProperty
from kivy.uix.screenmanager import ScreenManager

from gui.screens import ConnectedScreen, AgentScreen, LoginScreen


# MARK: TODOs
# TODO: Implement a way to dynamically load a scrolling view of the BBBs (Kivy Recycleview?)
# TODO: Implement the service to connect to the agent via ssh (naw, do so via the REST endpoints) -- fix screen as well


# MARK: Config and load appropriate kv file
Builder.load_file('kv/screens.kv')


class ProjectAuxoApp(App):
    icon = 'assets/Auxo_Logo_Black.png'
    title = 'Project Auxo Platform'

    username = StringProperty("")
    password = StringProperty("")
    agent_name = StringProperty("")

    alive_agents = DictProperty(None)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(LoginScreen.LoginScreen(name='login_screen'))
        manager.add_widget(ConnectedScreen.ConnectedScreen(name='connected_screen'))
        manager.add_widget(AgentScreen.AgentScreen(name='agent_screen'))

        return manager


if __name__ == '__main__':
    ProjectAuxoApp().run()
