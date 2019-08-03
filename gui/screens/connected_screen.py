"""
Displays the state of the various agents alive on the network
"""
from kivy.uix.label import Label
from kivy.clock import mainthread
from kivy.properties import StringProperty
from kivy.uix.screenmanager import SlideTransition, Screen

from gui.kvhelpers import HoverButton

from zmq.error import ZMQError
import threading
from functools import partial

from auxo_olympus.lib.mdbroker import MajorDomoBroker
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

    def _show_toast(self, text):
        self.ids['toast'].show(text, expiry_time=2)

    def on_enter(self):
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
            agent_status = status[boolean]
            self.registered_agent_labels[agent_name] = Label(
                text=f'{agent_name}: {agent_status}',
                halign='left',
                color=[0, 0, 0, 1],
                size_hint=(1, 1/3)
            )
            self.registered_agent_buttons[agent_name] = HoverButton(
                text='connect',
                background_normal='assets/green.png' if boolean else 'assets/red.png',
                size_hint=(1, 1/3),
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
            self.reset()

    def launch_broker(self, *args):
        self.broker_addr: str = args[0]

        self.broker_thread = MajorDomoBroker(verbose=True)
        try:
            self.broker_thread.bind(f"tcp://{self.broker_addr}")
            self.broker_thread.start()

            self.ids['broker_status_label'].text = f"broker at: {self.broker_addr}"
        except ZMQError as e:
            self._show_toast(repr(e))

            self.broker_thread.shutdown_flag.set()
            if self.broker_thread.is_alive():
                self.broker_thread.join(0.0)
            self.broker_thread = None

    def reset(self):
        self.ids['broker_addr_input'].text = ''
        self.ids['loading_circle'].source = 'assets/loading_circle.gif'
        self.ids['loading_circle'].anim_delay = 1/20

        # Delete all the dynamically placed widget as well
        for agent_name, _ in self.registered_agents.items():
            self.ids['bbb_grid_label'].remove_widget(self.registered_agent_labels[agent_name])
            self.ids['bbb_grid_connect_button'].remove_widget(self.registered_agent_buttons[agent_name])

        self.registered_agents.clear()

        if self.broker_thread:
            self.broker_thread.shutdown_flag.set()
            self.broker_thread.join(0.0)
            self.broker_thread = None

            self.ids['broker_status_label'].text = f"broker at: "
