from socket import socket, SOL_SOCKET, SO_REUSEADDR, AF_INET, SOCK_DGRAM
import threading
import os
import struct

# Create a server UDP socket and allow address re-use
s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 5000))

class RequestHandler(threading.Thread):
    def __init__(self, client_id, address):
        threading.Thread.__init__(self)
        self.client_id = client_id
        self.address = address

    def run(self):
        # Send file name message to client
        s.sendto('1'.encode(), self.address)

        # Receive 'Ready' message from client
        ready_msg_bytes, addr = s.recvfrom(1024)
        ready_msg = ready_msg_bytes.decode()
        print(f"Client {self.client_id}: {ready_msg}")

        # Send file size to client
        file_size = os.path.getsize("files/100MB.bin")
        file_size_bytes = struct.pack("!Q", file_size)
        s.sendto(file_size_bytes, self.address)

        # Send file data to client
        with open("files/100MB.bin", "rb") as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                s.sendto(data, self.address)

        print(f"Client {self.client_id}: File sent")

print("Starting server")
while True:
    # Receive client ID from client
    client_id_bytes, addr = s.recvfrom(1024)
    client_id = int(client_id_bytes.decode())

    # Start a new thread to handle the client request
    request_handler = RequestHandler(client_id, addr)
    request_handler.start()