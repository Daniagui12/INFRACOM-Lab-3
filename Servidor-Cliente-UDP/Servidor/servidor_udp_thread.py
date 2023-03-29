import socket

server_address = ('localhost', 8000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)

while True:
    # Create a dictionary to store received packets
    received_packets = {}
    client_id = None

    while True:
        # Receive a packet from the client
        packet, client_address = server_socket.recvfrom(1024)

        # Extract the client id and sequence number from the packet
        parts = packet.decode().split(':', 2)
        print(parts)
        if len(parts) == 3:
            client_id = int(parts[2])
            sequence_number = int(parts[0])
            message = parts[1]
            print(f"Received packet {sequence_number} from client {client_id} at {client_address}: {message}")
        else:
            print(f"Received invalid packet from {client_address}: {packet.decode()}")
            continue

        # Store the packet in the dictionary
        received_packets[sequence_number] = message

        # Send an acknowledgement for this packet
        server_socket.sendto(f"ACK:{sequence_number}:{client_id}".encode(), client_address)

        # Check if we have received all packets
        if len(received_packets) == 10:
            # Reassemble the packets in order and print the result
            message = ''.join(received_packets[i] for i in range(1, 11))
            print(f"Received message from client {client_id} at {client_address}: {message}")
            break