
from netmiko import ConnectHandler
from netmiko.cisco import *
from netmiko.cisco_base_connection import *

import logging
logging.basicConfig(filename='cedge_basic.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

cedge = {
    'device_type': 'cisco_ios',
    'ip': '192.168.50.53',
    'username': 'admin',
    'password': 'sdnlabs2324#',
}

net_connect = CiscoBaseConnection(**cedge)
output = net_connect.send_command('show ip int brief')
print (output)

net_connect.enable()

# Changing config_mode from regular 'config t' to 'config-transaction'
net_connect.config_mode('config-transaction')

# Config command in list. Make sure to add 'commit' at end.
cmd = ['int Loopback 0', 'ip address 1.1.1.44 255.255.255.255', 'commit']

output = net_connect.send_config_set(cmd)
print (output)
