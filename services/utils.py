import netifaces


def get_network_interfaces(nic_name=None):
    '''
     Determine the IP address of  the network interfaces
     Return a tuple of list of global IP addresses, list of MAC addresses, and local IP address
     '''
    local = None
    ip_address_list = []
    mac_address_list = []
    if_name_list = []
    if_names = netifaces.interfaces()
    for ifName in if_names:
        ifInfo = netifaces.ifaddresses(ifName)
        if netifaces.AF_INET in ifInfo:
            ifAddrs = ifInfo[netifaces.AF_INET]
            ifAddr = ifAddrs[0]['addr']
            if ifAddr == '127.0.0.1':
                local = ifAddr
            else:
                ip_address_list.append(ifAddr)
                if_name_list.append(ifName)
                linkAddrs = netifaces.ifaddresses(ifName)[netifaces.AF_LINK]
                linkAddr = linkAddrs[0]['addr'].replace(':', '')
                mac_address_list.append(linkAddr)
                if nic_name == ifName:
                    ip_address_list = [ip_address_list[-1]]
                    mac_address_list = [mac_address_list[-1]]
                    break

    return ip_address_list, mac_address_list, if_name_list, local


if __name__ == '__main__':
    print(get_network_interfaces())
