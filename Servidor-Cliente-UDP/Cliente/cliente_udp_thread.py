import datetime
import socket
import struct
import threading
import time
BUFF_SIZE = 65507
log_filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + "-log.txt"

def receive_file(client_socket, file_size, client_id, num_clients, host, port_udp):
    file_name = f"ArchivosRecibidos/Cliente{client_id+1}-Prueba-{num_clients}.txt"
    file_size2 = file_size

    # Reescribimos el archivo en un archivo con el nombre "Cliente"
    check_sum = 0
    with open(file_name, 'wb') as f:
        start_time = time.monotonic()
        while file_size > 0:
            # Make condition in order to recvfrom doesnt block the thread
            if file_size < BUFF_SIZE:
                data, _ = client_socket.recvfrom(file_size)
            else:
                data, _ = client_socket.recvfrom(BUFF_SIZE)

            # Revisamos el fin del archivo
            if len(data) == 0 or data == b'':
                break
            f.write(data)
            file_size -= len(data)
            check_sum += len(data)
            print(f"Received {len(data)} bytes from server for client {client_id}.")

        end_time = time.monotonic()
        # Calcular el tiempo total de recepción
        tiempo_total = end_time - start_time

        if check_sum == file_size2:
            with open(f"Logs/{log_filename}", 'a') as log_file:
                log_file.write(f"Client {client_id+1}: file=Cliente{client_id+1}-Prueba-{num_clients}.txt, size={check_sum}, status=SUCCESS, time={tiempo_total} seconds\n")
        else: 
            with open(f"Logs/{log_filename}", 'a') as log_file:
                log_file.write(f"Client {client_id+1}: file=Cliente{client_id+1}-Prueba-{num_clients}.txt, size={check_sum}, status=FAIL, time={tiempo_total} seconds\n")
    

    print(f"Received file from server for client {client_id} in {tiempo_total} seconds.")

def send_message(id, host, port, message, num_clients, port_udp):
    client_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client_socket_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Connect to the ip over the given port
    client_socket_tcp.connect((host, port))

    client_socket_udp.bind((host, 0))

    # Send the file size we want to the server with a sequence number
    while True:
        data = f"{message}:{id}"
        client_socket_tcp.send(data.encode())
        print(f"Sent client id {id} and file size {message} to server at {host}:{port}")

        # Receive the file
        # Extract the client id and sequence number from the packet
        packet = client_socket_tcp.recv(1024)
        parts = packet.decode().split(':')
        if len(parts) == 2:
            client_id = int(parts[1])
            file_size = parts[0]
        
        print(f"Received file size {file_size} from server for client {client_id}")

        port_client_udp = client_socket_udp.getsockname()[1]

        port_bytes = struct.pack('>i', port_client_udp)

        # Now we send the port that the client is connected to
        client_socket_tcp.send(port_bytes)

        receive_file(client_socket_udp, int(file_size), client_id, num_clients, host, port_udp)
        break


try:
    if __name__ == '__main__':
        host = 'localhost'
        port = 5000
        port_udp = 8000
        file_num = input("Enter the file number to send (1 for 100MB or 2 for 250MB): ")
        num_clients = int(input("Enter the number of clients to send the file to (Max 25): "))

        if file_num != '1' and file_num != '2':
            print("Invalid file number")
            exit()

        if num_clients > 25:
            print("Max number of clients is 25")
            exit()

        # create 10 threads and send messages concurrently
        for i in range(num_clients):
            thread = threading.Thread(target=send_message, args=(i, host, port, file_num, num_clients, port_udp))
            thread.start()

except KeyboardInterrupt:
    print("Keyboard interrupt")
    exit()