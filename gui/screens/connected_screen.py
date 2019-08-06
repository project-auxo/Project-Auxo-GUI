"""
Displays the state of the various agents alive on the network
"""
from kivy.uix.label import Label
from kivy.clock import mainthread
from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import SlideTransition, Screen

from gui.kvhelpers import HoverButton

from zmq.error import ZMQError
import threading
from functools import partial

from auxo_olympus.lib.entities.mdbroker import MajorDomoBroker
from services.discovery import SimpleDiscService


class ConnectedScreen(Screen):
    registered_agents = {}
    registered_agent_buttons = {}
    registered_agent_labels = {}
    broker_addr = StringProperty("")
    thread = None

    stop = threading.Event()

    def __init__(self, **kwargs):
        self.broker_thread = None
        super(ConnectedScreen, self).__init__(**kwargs)

    def _show_toast(self, text, color='red'):
        if color == 'red':
            pass        # Toast banner is red by default

        elif color == 'green':
            green_rgba = [0.247, 0.890, 0.149]
            self.ids['toast'].change_color(color=green_rgba)

        self.ids['toast'].show(text, expiry_time=2)

    def on_enter(self):
        if self.registered_agents:
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
        num_agents = len(self.registered_agents)
        status = {True: 'online', False: 'offline'}

        for agent_name, boolean in self.registered_agents.items():
            agent_status = status[boolean]
            self.registered_agent_labels[agent_name] = Label(
                text=f'{agent_name}: {agent_status}',
                halign='justify',
                color=[0, 0, 0, 1],
                size_hint=(1, 1/num_agents)
            )
            self.registered_agent_buttons[agent_name] = HoverButton(
                text='connect',
                background_normal='assets/green.png' if boolean else 'assets/red.png',
                size_hint=(1, 1/num_agents),
               on_press=partial(self.connect_to_agent, agent_name, boolean)
            )

            self.ids['bbb_grid_label'].add_widget(self.registered_agent_labels[agent_name])
            self.ids['bbb_grid_connect_button'].add_widget(self.registered_agent_buttons[agent_name])

    @mainthread
    def do_logout(self):
        self.manager.transition = SlideTransition(direction='right')
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

            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'agent_screen'

            if self.broker_thread:
                self.reset(kill_broker=False)

    def launch_broker(self, *args):
        self.broker_addr: str = args[0]

        self.broker_thread = MajorDomoBroker(verbose=True)
        try:
            assert threading.Thread in type(self.broker_thread).__bases__
            self.broker_thread.bind(f"tcp://{self.broker_addr}")
            self.broker_thread.start()

        except ZMQError as e:
            self._show_toast(repr(e))
            self.quit_broker()      # cleanup

        self._show_toast(text=f'broker - {self.broker_addr} launched!', color='green')

    def quit_broker(self):
        self.ids['broker_addr_input'].text = ''

        if self.broker_thread:
            self.broker_thread.shutdown_flag.set()
            if self.broker_thread.is_alive():
                self.broker_thread.join(0.0)
            self.broker_thread = None

            self._show_toast(text=f'broker - {self.broker_addr} killed!')

    def switch_to_broker(self):
        if self.broker_thread:
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'broker_screen'
            self.reset(kill_broker=False)

    def reset(self, kill_broker: bool = True):
        self.ids['loading_circle'].source = 'assets/loading_circle.gif'
        self.ids['loading_circle'].anim_delay = 1/20

        # Delete all the dynamically placed widget as well
        for agent_name, _ in self.registered_agents.items():
            self.ids['bbb_grid_label'].remove_widget(self.registered_agent_labels[agent_name])
            self.ids['bbb_grid_connect_button'].remove_widget(self.registered_agent_buttons[agent_name])

        self.registered_agents.clear()
        if kill_broker:
            self.quit_broker()

