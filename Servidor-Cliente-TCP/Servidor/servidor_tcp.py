import socket
import selectors
import sys
import signal

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((sys.argv[1], int(sys.argv[2])))

    server_socket.listen()
    print(f'Server ready and listening on {sys.argv[1]}:{sys.argv[2]}')

except socket.error as e:
    print(f'Error creating socket: {e}')
    sys.exit(1)


selector = selectors.DefaultSelector()

def accept(sock, mask):

    conn, addr = sock.accept()
    conn.setblocking(False)
    print(f'Accepted connection from {addr}')

    selector.register(conn, selectors.EVENT_READ, data=None)

def read(conn, mask):

    with open('file_received.txt', 'wb') as f:
        data = conn.recv(1024)
        while data:
            f.write(data)
            data = conn.recv(1024)
    print(f'File received from {conn.getpeername()}')
    selector.unregister(conn)
    conn.close()

selector.register(server_socket, selectors.EVENT_READ, data=None)

def handle_sigint(signum, frame):
    print('Server closed')
    server_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_sigint)

try:
    while True:
        
        events = selector.select(timeout=1)

        for key, mask in events:

            conn = key.fileobj

            if conn == server_socket:
                accept(conn, mask)
            else:
                read(conn, mask)
        
        if not selector.get_map():
            break

except KeyboardInterrupt:
    handle_sigint(signal.SIGINT, None)


