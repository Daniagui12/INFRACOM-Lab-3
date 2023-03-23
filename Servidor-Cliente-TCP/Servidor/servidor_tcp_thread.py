from socket import SO_REUSEADDR, SOCK_STREAM, error, socket, SOL_SOCKET, AF_INET
import logging
import hashlib
import os
import datetime
import sys
from threading import Thread, Lock
from queue import Queue

thread_lock = Lock()

# Create a server TCP socket and allow address re-use
s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 65432))

# Create a list in which threads will be stored in order to be joined later
threads = []

class RequestHandler(Thread):
    def __init__(self, msg, addr, port, s, lock, file_num):
        Thread.__init__(self)
        self.port = port
        self.addr = addr
        self.s = s
        self.lock = lock
        self.msg = msg
        self.file_num = file_num

        # Define the actions the thread will execute when called.
    def run(self):

        # Get the message from the client
        print(f"Message received from client {self.addr}: {self.msg}")

        # if message from client is "Ready", send the file
        if self.msg == "Ready":
            self.send_file()
        
        else:
            print("Message not recognized")
        
        # Close the connection
        self.s.close()


    def send_file(self):
        
        if self.file_num == 1:
            file_name = "files/100MB.bin"
        
        elif self.file_num == 2:
            file_name = "files/250MB.bin"

        file_hash = hashlib.md5(open(file_name, 'rb').read()).hexdigest()

        # Send the file hash
        self.s.send(file_hash.encode())

        # Send the file size
        file_size = os.path.getsize(file_name)
        self.s.send(str(file_size).encode())

        # Send the file
        with open(file_name, 'rb') as f:
            start_time = datetime.datetime.now()
            remaining_bytes = file_size
            while remaining_bytes > 0:
                # Send 1024 bytes at a time
                data = f.read(1024)
                self.s.send(data)
                remaining_bytes -= 1024
            end_time = datetime.datetime.now()
            print(f"File sent to client {self.addr} in {end_time - start_time}")


file_num = int(input("Enter the file number to send (1 for 100MB or 2 for 250MB): "))
print("Starting server")
# Continuously listen for a client request and spawn a new thread to handle every request
while True:

    try:

        print("Waiting for a client request")
        # Listen for a request
        s.listen(1)
        # Accept the request
        sock, addr = s.accept()

        # Receive the message from the client
        response_message = sock.recv(1024).decode()

        # Spawn a new thread for the given request
        newThread = RequestHandler(response_message, addr[0], addr[1], sock, thread_lock, file_num)
        newThread.start()
        threads.append(newThread)

    except KeyboardInterrupt:
        print ("\nExiting Server\n")
        break

# When server ends gracefully (through user keyboard interrupt), wait until remaining threads finish
for item in threads:
    item.join()