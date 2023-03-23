from socket import SO_REUSEADDR, SOCK_STREAM, error, socket, SOL_SOCKET, AF_INET
import selectors
import types
import logging
import hashlib
import os
import datetime
import time
from threading import Thread
from queue import Queue

num_clients = 2

class ClientThread:
    def __init__(self, id, address, port, log_filename):
        self.id = id
        self.address = address
        self.port = port
        self.s = socket(AF_INET, SOCK_STREAM)
        self.log_filename = log_filename


    def run(self):
        global num_clients
        try:
            # Timeout if the no connection can be made in 5 seconds
            self.s.settimeout(5)
            # Allow socket address reuse
            self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            # Connect to the ip over the given port
            self.s.connect((self.address, self.port))
            # Send the defined request message
            message = "Ready"

            self.s.send(message.encode())

            # Receive the file hash
            file_hash = self.s.recv(1024).decode()
            print(f'Hash received from server for client {self.id}: {file_hash}')

            # Receive the file size
            file_size = int(self.s.recv(1024).decode())
            print(f"File size received from server for client {self.id}: {file_size} bytes")

            self.receive_file(file_size, file_hash, num_clients)
            
            self.s.close()
        except error as e:
            print(e)
            raise(e)


    def receive_file(self, file_size, file_hash, num_clients):
        
        client_id = self.id

        with open(f"ArchivosRecibidos/Cliente{client_id+1}-Prueba-{num_clients}.txt", 'wb') as f:
            start_time = datetime.datetime.now()
            remaining_bytes = file_size
            while remaining_bytes > 0:
                chunk_size = min(4096, remaining_bytes)
                data = self.s.recv(chunk_size)
                #print(f"Received {len(data)} bytes from server for client {client_id}.")
                f.write(data)
                remaining_bytes -= len(data)
            end_time = datetime.datetime.now()
            time_diff = end_time - start_time
            print(f"Received {file_size} bytes from server for client {client_id} in {time_diff.total_seconds()} seconds.")

            hash_obj = hashlib.sha256()
            with open(f.name, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    hash_obj.update(data)
            calculated_hash = hash_obj.hexdigest()
            if calculated_hash == file_hash:
                print(f"Hash of received file matches the hash received from server for client {client_id}.")
                status = "SUCCESS"
            else:
                print(f"Hash of received file does not match the hash received from server for client {client_id}.")
                status = "FAILED"
            with open(f"Logs/{self.log_filename}", 'a') as log_file:
                log_file.write(f"Client {client_id+1}: file=Cliente{client_id+1}-Prueba-{num_clients}.txt, size={file_size}, status={status}, time={time_diff.total_seconds()} seconds\n")


# Create a queue to hold the tasks for the worker threads
q = Queue(maxsize=0)


# Function which generates a Client instance, getting the work item to be processed from the queue
def worker():
    while True:
        try:
            item = q.get()
            client = ClientThread(item, "127.0.0.1", 65432, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + "-log.txt")
            client.run()
        except Exception as e:
            logging.exception(f"Exception in worker: {e}")
        finally:
            q.task_done()

#--------------------------------------------------#
########## INITIATE CLIENT WORKER THREADS ##########
#--------------------------------------------------#

# Populate the work queue with a list of numbers as long as the total number of requests wished to be sent.
# These queue items can be thought of as decrementing counters for the client thread workers.
for item in range(2):
    q.put(item)

# Create a number of threads, given by the maxWorkerThread variable, to initiate clients and begin sending requests.
for i in range(2):
    t = Thread(target=worker)
    t.daemon = True
    t.start()

# Do not exit the main thread until the sub-threads complete their work queue
q.join()