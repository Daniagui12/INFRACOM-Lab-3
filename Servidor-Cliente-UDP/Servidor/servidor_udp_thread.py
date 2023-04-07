import datetime
import logging
import os
import socket
import struct
import time
from socket import SO_REUSEADDR, SOCK_DGRAM, SOCK_STREAM, error, socket, SOL_SOCKET, AF_INET

server_address_tcp = ('localhost', 5000)
server_address_udp = ('localhost', 8000)
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(server_address_udp)
BUFF_SIZE = 65507

# Create a server TCP socket and allow address re-use
s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(server_address_tcp)

def init_logger():
    log_dir = 'Servidor-Cliente-UDP/Servidor/Logs'
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    log_filename = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '-log.txt'
    logging.basicConfig(filename=f'Servidor-Cliente-UDP/Servidor/Logs/{log_filename}', level=logging.INFO)
    return logging.getLogger()

logger = init_logger()

def send_file_udp(id, file_size, client_address, sock):

    if file_size == 1:
        file_name = "100MB.bin"
        file_size = os.path.getsize(f"files/{file_name}")
    else:
        file_name = "250MB.bin"
        file_size = os.path.getsize(f"files/{file_name}")

    while True:
        data = f"{file_size}:{id}"
        sock.send(data.encode())
        print(f"Sent packet {file_size} to client at {client_address} with client id {id}")
        break

    port_bytes = sock.recv(4)
    port_to_use = struct.unpack('>i', port_bytes)[0]
    
    client_address = (client_address[0], port_to_use)
    bytes_sent = 0
    # Send the file contents
    with open(f"files/{file_name}", "rb") as f:
        start = time.monotonic()
        while True:
            data = f.read(BUFF_SIZE)
            if not data:
                break
            server_socket.sendto(data, client_address)
            bytes_sent += len(data)
        end = time.monotonic()
        print(f"Sent file {file_name} of {file_size} bytes to client {id} at {client_address} and sent {bytes_sent} bytes in total.")

    # Log the time it took to send the file
    total = end - start
        
    logger.info(f"Sent file {file_name} of {file_size} bytes to client {id} at {client_address} and sent {bytes_sent} bytes in total. Took {total} seconds to send the file.")
    # Send an empty packet to signal the end of the file
    server_socket.sendto(b'', client_address)
    print(f"Sent end of file to client at {client_address} with client id {id}")
        

try:
    print("Server is listening on port 8000 and TCP on port 5000...")
    print("Waiting for client to connect...")
    while True:
        # Create a dictionary to store received packets
        client_id = None

        while True:
            # Listen for a request
            s.listen()
            # Accept the request
            sock, client_address = s.accept()
            # Receive a packet from the client
            packet = sock.recv(1024)

            # Extract the client id and sequence number from the packet
            parts = packet.decode().split(':')
            if len(parts) == 2:
                client_id = int(parts[1])
                message = parts[0]
                print(f"Received packet from client {client_id} at {client_address}: {message}")
            else:
                print(f"Received invalid packet from {client_address} with client id {client_id}: {packet.decode()}")
                continue

            # # Send an acknowledgement for this packet
            # server_socket.sendto(f"ACK:{sequence_number}:{client_id}".encode(), client_address)

            # Send the file
            if message == "1" or message == "2":
                send_file_udp(client_id, int(message), client_address, sock)
                break
        

except KeyboardInterrupt:
    print("Server shutting down...")
    server_socket.close()
    s.close()