""" All the endpoints """

led_endpoint = lambda selected_agent_ip: f"http://{selected_agent_ip}:5000/change_led_status"
