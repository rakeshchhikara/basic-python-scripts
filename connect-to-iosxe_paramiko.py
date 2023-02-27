import paramiko

# creating an ssh client object
ssh_client = paramiko.SSHClient()
# print(type(ssh_client))

ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print('Connecting to 10.197.249.82')
ssh_client.connect(hostname='10.197.249.82', port='22', username='admin', password='cisco!123',
                   look_for_keys=False, allow_agent=False)


# checking if the connection is active
conn_status = ssh_client.get_transport().is_active()
print(f'SSH connection status: {conn_status}')

# sending commands
# ...

print('Closing connection')
ssh_client.close()
