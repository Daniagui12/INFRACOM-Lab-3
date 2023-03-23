

import os
import time


bufferSize = 65535
numClientes = 25

def recibir(clientSocket, clientAddress, clientId, fileSize):
    print(f'Receiving file from {clientAddress} (client {clientId})...')
    tiempoInicio = time.time()
    data = b''
    while len(data) < fileSize:
        packet = clientSocket.recv(bufferSize)
        if not packet:
            break
        else:
            data += packet
    tiempoFin = time.time()
    tiempoTranscurrido = tiempoFin - tiempoInicio
    if len(data) == fileSize:
        file_name = f'{clientId}-Prueba-{numClientes}.txt'
        with open(os.path.join('ArchivosRecibidos', file_name), 'wb') as f:
            f.write(data)
        print(f'File received from {clientAddress} (client {clientId}): {file_name} ({fileSize} bytes, {tiempoTranscurrido:.2f} seconds)')
        return True, tiempoTranscurrido
    else:
        print(f'Error receiving file from {clientAddress} (client {clientId})')
        return False, None