import socket
import selectors
import sys

def create_client_socket(server_address, server_port):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((server_address, server_port))

    return client_socket


def read(client_socket, mask):

    message = client_socket.recv(1024)
    if message:
        print(f'Received: {message.decode()}')
    else:
        print(f'Connection closed by server')
        selector.unregister(client_socket)
        client_socket.close()

def write(client_socket, mask):

    with open('file.txt', 'rb') as f:
        data = f.read(1024)
        while data:
            client_socket.send(data)
            data = f.read(1024)
    print('File sent to server')
    selector.unregister(client_socket)
    client_socket.close()

selector = selectors.DefaultSelector()

n = int(sys.argv[3])
for i in range(n):
    client_socket = create_client_socket(sys.argv[1], int(sys.argv[2]))
    selector.register(client_socket, selectors.EVENT_WRITE, data=None)

while True:
    # Wait for events on the registered sockets
    events = selector.select()

    for key, mask in events:

        if mask & selectors.EVENT_READ:
            read(key.fileobj, mask)
        if mask & selectors.EVENT_WRITE:
            write(key.fileobj, mask)
    
    if len(selector.get_map()) == 0:
        break

for key, mask in selector.get_map().items():
    key.fileobj.close()