from netmiko import ConnectHandler

# Define device information
device = {
    'device_type': 'cisco_xe',
    'ip': '10.197.249.82',
    'username': 'admin',
    'password': 'cisco!123',
    'port': 22,
    'secret': 'cisco!123'
}

# Connect to device
with ConnectHandler(**device) as conn:
    # Enter enable mode
    conn.enable()

    # Run command
    output = conn.send_command('show version')

    # Print output
    print(output)
