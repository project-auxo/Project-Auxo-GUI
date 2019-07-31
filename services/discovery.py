import re
import os
import platform
import subprocess
import threading
from typing import Dict, List, Any

from services.utils import get_network_interfaces


class SimpleDiscService(object):
    """
    Simple class to find known hosts
    """
    def __init__(self):
        self.ip_address: List[Any] = None
        self.mac_address: List[Any] = None

        dirname: str = os.path.dirname(__file__)
        self.file_path: str = os.path.join(dirname, '../config/riaps-hosts.conf')

    def registered_agents(self) -> Dict[str, bool]:
        self.setup_interfaces()
        with open(self.file_path, 'r') as f:
            out: List[str] = f.readlines()

        # some minimal parsing to extract the bbb names
        out = re.sub(r'.*=\s', '', out[3]).split(',')
        return self.ping_all_agents(out)

    def setup_interfaces(self) -> None:
        global_IPs, global_MACs, _global_names, _local_ip = get_network_interfaces()

        assert len(global_IPs) > 0, f"Error: no active network interfaces to use"
        self.ip_address = global_IPs[0]
        self.mac_address = global_MACs[0]

    def ping_all_agents(self, agent_names: List[str]) -> Dict[str, bool]:
        """
        Ping all the known agents and note them as alive, note that I use the words host and agent interchangeably
        :return:
        """
        agent_map: Dict[str, bool] = {}
        threads: List[threading.Thread] = []
        for agent in agent_names:
            t = threading.Thread(target=self.ping, args=(agent, agent_map), name=f'Ping-{agent}-Thread')
            threads.append(t)
            t.start()

        for thread in threads:
            thread.join()

        return agent_map

    def ping(self, agent: str, agent_map: dict):
        param = '-n' if platform.system() == 'windows' else '-c'
        command = ['ping', param, '1', agent]

        try:
            agent_status = subprocess.call(command, stdout=subprocess.DEVNULL, timeout=0.8) == 0     # DEVNULL to suppress output
        except subprocess.TimeoutExpired:
            agent_status = False

        agent_map[agent] = agent_status


if __name__ == '__main__':
    S = SimpleDiscService()

    # Simple test for SimpleDiscService()
    print(S.ping_all_agents(['bbb-df1f.local', 'bbb-0328.local', 'bbb-4444.local']))
