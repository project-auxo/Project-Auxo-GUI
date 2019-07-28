from kivy.clock import mainthread
from kivy.uix.screenmanager import SlideTransition, Screen
from kivy.uix.label import Label

from gui.kvhelpers import HoverButton

import threading
from functools import partial
from services.discovery import SimpleDiscService


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
                                                               on_press=partial(self.connect_to_agent, agent_name, boolean))

            self.ids['bbb_grid_label'].add_widget(self.registered_agent_labels[agent_name])
            self.ids['bbb_grid_connect_button'].add_widget(self.registered_agent_buttons[agent_name])

    @mainthread
    def do_logout(self):
        self.manager.transition = SlideTransition(direction='down')
        self.manager.current = 'login_screen'
        self.reset()
        self.stop.set()

    def connect_to_agent(self, *args):
        # Perform transition -- connect at destination
        selected_agent_name: str = args[0].strip()      # remove the leading and trailing spaces
        agent_online: bool = args[1]

        if agent_online:
            agent_screen = self.manager.get_screen('agent_screen')
            setattr(agent_screen, 'selected_agent_name', selected_agent_name)

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
