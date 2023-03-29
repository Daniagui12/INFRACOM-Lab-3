import socket
import threading

def send_message(id, host, port, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send the file size we want to the server with a sequence number
    sequence_number = 0
    while True:
        sequence_number += 1
        data = f"{sequence_number}:{message}:{id}"
        client_socket.sendto(data.encode(), (host, port))
        response, server_address = client_socket.recvfrom(1024)
        if response.decode() == f"ACK:{sequence_number}:{id}":
            # Received acknowledgement for this packet, move on to the next one
            print(f"Received acknowledgement for packet {sequence_number} from server at {server_address}")
            break

    client_socket.close()

if __name__ == '__main__':
    host = 'localhost'
    port = 8000
    file_num = input("Enter the file number to send (1 for 100MB or 2 for 250MB): ")

    # create 10 threads and send messages concurrently
    for i in range(10):
        thread = threading.Thread(target=send_message, args=(i, host, port, file_num))
        thread.start()