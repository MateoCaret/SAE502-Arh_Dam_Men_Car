# import paramiko

# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# ssh.connect("192.168.1.55", username="user", password="bonjour")
# ssh.exec_command("ifstat > test.txt")
# ssh.exec_command("cat test.txt")

import paramiko, time

def get_network_usage():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("changer par l'adresse ip", username="user", password="bonjour")

    stdin, stdout, stderr = ssh.exec_command("ifstat 1 1")

    res = stdout.read().decode().strip().split('\n')
    # print(res)
    kb_in = res[2].split()[0]
    kb_out = res[2].split()[1]
    # print(f"in : {kb_in}, out : {kb_out}")

    ssh.close()
    return kb_in, kb_out

print(get_network_usage())

"""code qui peut servir si jamais on décide d'installer un agent sur le client

# import psutil

# def network_usage():
#     # Get network io statistics
#     net_io = psutil.net_io_counters()
#     mega_bytes_sent = net_io.bytes_sent // 1000000
#     mega_bytes_received = net_io.bytes_recv // 1000000
#     packets_sent = net_io.packets_sent
#     packets_received = net_io.packets_recv

#     print(f"Bytes sent: {mega_bytes_sent} Mo")
#     print(f"Bytes received: {mega_bytes_received} Mo")
#     print(f"Packets sent: {packets_sent}")
#     print(f"Packets received: {packets_received}")
    
#     return mega_bytes_sent, mega_bytes_received, packets_sent, packets_received

# print(network_usage())
# test = network_usage()
# print(test[0])

# import psutil
# import socket
# import json

# def network_usage():
#     # Get network io statistics
#     net_io = psutil.net_io_counters()
#     mega_bytes_sent = net_io.bytes_sent // 1000000
#     mega_bytes_received = net_io.bytes_recv // 1000000
#     packets_sent = net_io.packets_sent
#     packets_received = net_io.packets_recv

#     return mega_bytes_sent, mega_bytes_received, packets_sent, packets_received

# def send_data(host='localhost', port=12345):
#     # Create a socket object
#     s = socket.socket()

#     # Connect to the server
#     s.connect((host, port))

#     # Send data
#     s.send(json.dumps(network_usage()).encode('utf-8'))

#     # Close the connection
#     s.close()

# send_data()

# import socket
# import json

# def receive_data(port=12345):
#     # Create a socket object
#     s = socket.socket()

#     # Bind to the port
#     s.bind(('', port))

#     # Put the socket into listening mode
#     s.listen(5)

#     while True:
#         # Establish a connection with the client
#         c, addr = s.accept()

#         # Receive data from the client
#         data = c.recv(1024)
#         if data:
#             print(json.loads(data.decode('utf-8')))

#         # Close the connection with the client
#         c.close()

# receive_data()"""