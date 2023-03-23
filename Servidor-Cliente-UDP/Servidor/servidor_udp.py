
import datetime
import logging
import socket
import sys


log_filename = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '-log.txt'
logging.basicConfig(filename=f'Logs/{log_filename}', level=logging.INFO)

buffeSize = 65507 
file100MB = 'archivo_100MB'
file250MB = 'archivo_250MB'
numConexiones = 25

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((sys.argv[1], int(sys.argv[2])))

    serverSocket.listen()
    print(f'Server ready and listening on {sys.argv[1]}:{sys.argv[2]}')

except socket.error as e:
    print(f'Error creating socket: {e}')
    sys.exit(1)

def enviarArchivo(file_path, addr):

    with open(file_path, 'rb') as f:
        chunk = f.read(buffeSize)
        tiempoInicio = datetime.datetime.now()
        while chunk:
            serverSocket.sendto(chunk, addr)
            chunk = f.read(buffeSize)
        tiempoFin = datetime.datetime.now()

    timpoTransferencia = tiempoFin - tiempoInicio
    file_size = f.tell()
    logging.info(f'Archivo {file_path} ({file_size} bytes) enviado a {addr}. Tiempo de transferencia: {timpoTransferencia}')

while True:
    data, addr = serverSocket.recvfrom(buffeSize)
    logging.info(f'Nueva conexión de {addr}')

    cmd = data.decode()
    logging.info(f'Comando recibido: {cmd}')

    if cmd == '100':
        enviarArchivo(file100MB, addr)
    elif cmd == '250':
        enviarArchivo(file250MB, addr)
