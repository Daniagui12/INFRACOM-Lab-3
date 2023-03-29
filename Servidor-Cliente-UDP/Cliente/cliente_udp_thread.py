from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import time

SERVER_ADDRESS = ('127.0.0.1', 5000)
NUM_CLIENTS = 25

class Client(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.id = id

    def run(self):
        s = socket(AF_INET, SOCK_DGRAM)

        # Send client ID to server
        s.sendto(str(self.id).encode(), SERVER_ADDRESS)

        # Receive file name message from server
        file_name_msg, addr = s.recvfrom(1024)
        print(f"Client {self.id}: Received file name message {file_name_msg.decode()}")

        # Send 'Ready' message to server
        s.sendto('Ready'.encode(), SERVER_ADDRESS)

        # Receive file size from server
        file_size_bytes, addr = s.recvfrom(1024)
        file_size = int.from_bytes(file_size_bytes, byteorder='big')
        print(f"Client {self.id}: Received file size {file_size}")

        # Receive file data from server
        with open(f"ArchivosRecibidos/client_{self.id}.txt", "wb") as f:
            while True:
                data, addr = s.recvfrom(1024)
                if not data:
                    break
                f.write(data)

        print(f"Client {self.id}: File received")

        s.close()

print("Starting clients")
for i in range(NUM_CLIENTS):
    client = Client(i)
    client.start()

print("All clients started")