"""
Screen when connected to a given agent
"""

from kivy.uix.screenmanager import SlideTransition, Screen

import requests
import endpoints as ep

# MARK: Globals
led_value = 0
selected_agent = None


class AgentScreen(Screen):   # show the agent's vitals -- along with some minimal control

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'connected_screen'

    def toggle_led(self):
        global led_value
        led_value = int(not led_value)

        # interface with the rest endpoints
        url = ep.led_endpoint(self.selected_agent_name)
        try:
            _ = requests.post(url=url, data={'status': led_value})
        except Exception as e:
            print(f"Are you sure the service is running on the BBB?: {e}")

    def launch_worker(self):
        pass