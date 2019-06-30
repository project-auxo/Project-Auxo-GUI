from kivy.config import Config
Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '800')

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import mainthread
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.properties import StringProperty, DictProperty, BooleanProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, SlideTransition, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget

import threading
from services.discovery import SimpleDiscService


# MARK: TODOs
# TODO: Implement a way to dynamically load a scrolling view of the BBBs (Kivy Recycleview?)
# TODO: Implement the service to connect to the agent via ssh -- fix screen as well


# MARK: Extra Functionality
class MouseOver(Widget):
    def __init__(self, **kwargs):
        Window.bind(mouse_pos=self._mouse_move)
        self.hovering = BooleanProperty(False)
        self.poi = ObjectProperty(None)
        self.register_event_type('on_hover')
        self.register_event_type('on_exit')
        super(MouseOver, self).__init__(**kwargs)

    def _mouse_move(self, *args):
        if not self.get_root_window():
            return
        is_collide = self.collide_point(*self.to_widget(*args[1]))
        if self.hovering == is_collide:
            return
        self.poi = args[1]
        self.hovering = is_collide
        self.dispatch('on_hover' if is_collide else 'on_exit')

    def on_hover(self):
        pass

    def on_exit(self):
        pass


class HoverButton(Button, MouseOver):
    def on_hover(self):
        self.opacity = 0.85

    def on_exit(self):
        self.opacity = 1.0



# MARK: Extra Functionality
class MouseOver(Widget):
    def __init__(self, **kwargs):
        Window.bind(mouse_pos=self._mouse_move)
        self.hovering = BooleanProperty(False)
        self.poi = ObjectProperty(None)
        self.register_event_type('on_hover')
        self.register_event_type('on_exit')
        super(MouseOver, self).__init__(**kwargs)

    def _mouse_move(self, *args):
        if not self.get_root_window():
            return
        is_collide = self.collide_point(*self.to_widget(*args[1]))
        if self.hovering == is_collide:
            return
        self.poi = args[1]
        self.hovering = is_collide
        self.dispatch('on_hover' if is_collide else 'on_exit')

    def on_hover(self):
        pass

    def on_exit(self):
        pass


class HoverButton(Button, MouseOver):
    def on_hover(self):
        self.opacity = 0.85

    def on_exit(self):
        self.opacity = 1.0


# MARK: Screens
class ConnectedScreen(Screen):
    registered_agents = {}
    registered_agent_buttons = {}
    registered_agent_labels = {}
    thread = None

    stop = threading.Event()

    def on_enter(self):
        print('refreshing...')
        self.reset()

        self.thread = threading.Thread(
            target=self.get_agents_thread, args=()
        )
        self.thread.daemon = True
        self.thread.start()

    def get_agents_thread(self):
        self.registered_agents = SimpleDiscService().registered_agents()
        self.move_on()      # once thread has started there, move on

    @mainthread
    def move_on(self):
        self.ids['loading_circle'].source = 'assets/white.png'
        # self.ids['bbb_grid_label'].rows = len(self.registered_agents)
        # self.ids['bbb_grid_connect_button'].rows = len(self.registered_agents)
        num_agents = len(self.registered_agents)
        status = {True: 'online', False: 'offline'}

        for agent_name, boolean in self.registered_agents.items():
            if boolean:
                print(f'Beaglebone {agent_name} is online')
            else:
                print(f'Beaglebone {agent_name} is offline')

            agent_status = status[boolean]
            self.registered_agent_labels[agent_name] = Label(text=f'{agent_name}: {agent_status}', color=[0, 0, 0, 1], size_hint=(1, 1/num_agents))
            self.registered_agent_buttons[agent_name] = HoverButton(text='connect',
                                                               background_normal='assets/green.png' if boolean else 'assets/red.png',
                                                               size_hint=(1, 1/num_agents),
                                                               on_press=lambda _: self.connect_to_agent(agent_name))

            self.ids['bbb_grid_label'].add_widget(self.registered_agent_labels[agent_name])
            self.ids['bbb_grid_connect_button'].add_widget(self.registered_agent_buttons[agent_name])

    @mainthread
    def do_logout(self):
        self.manager.transition = SlideTransition(direction='down')
        self.manager.current = 'login_screen'
        self.reset()
        self.stop.set()

    def connect_to_agent(self, agent_name: str):
        # Attempting to connect
        self.manager.transition = SlideTransition(direction='down')
        self.manager.current = 'agent_screen'
        self.reset()

    def reset(self):
        self.ids['loading_circle'].source = 'assets/loading_circle.gif'
        self.ids['loading_circle'].anim_delay = 1/20

        # Delete all the dynamically placed widget as well
        for agent_name, _ in self.registered_agents.items():
            self.ids['bbb_grid_label'].remove_widget(self.registered_agent_labels[agent_name])
            self.ids['bbb_grid_connect_button'].remove_widget(self.registered_agent_buttons[agent_name])

        self.registered_agents.clear()


class AgentScreen(Screen):   # show the agent's vitals
    pass


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


# MARK: Config and load appropriate kv file
Builder.load_file('kv/screens.kv')


class ProjectAuxoApp(App):
    icon = 'assets/Auxo_Logo_Black.png'
    title = 'Project Auxo Agent Manager'

    username = StringProperty("")
    password = StringProperty("")
    agent_name = StringProperty("")

    alive_agents = DictProperty(None)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(LoginScreen(name='login_screen'))
        manager.add_widget(ConnectedScreen(name='connected_screen'))
        manager.add_widget(AgentScreen(name='agent_screen'))

        return manager


if __name__ == '__main__':
    Factory.register('MouseOver', MouseOver)
    ProjectAuxoApp().run()
