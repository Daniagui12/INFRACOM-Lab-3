import socket
import os
import logging
from datetime import datetime
import threading

#Tamaño maximo de bytes de paquetes UDP
bufferSize = 65535

# Dirección IP y puerto del servidor
server_address = ('157.253.220.113', 65432)

# Crear un socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Establecer un tiempo de espera para recibir datos del servidor
client_socket.settimeout(5)

# Directorio donde se van a almacenar los archivos recibidos
directory = 'ArchivosRecibidos'

# Directorio donde se van a almacenar los archivos de log
log_directory = 'Logs'


# Crear el directorio si no existe
if not os.path.exists(directory):
    os.makedirs(directory)

# Crear el directorio de logs si no existe
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configurar el logger para generar los archivos de log
log_filename = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-log.txt')
log_path = os.path.join(log_directory, log_filename)
logging.basicConfig(filename=log_path, level=logging.INFO,
                    format='%(asctime)s - %(message)s')

def solicitud(client_id,fileName,hilos):
    try:
        #Enviar un mensaje al servidor del archivo a solicitar
        client_socket.sendto(fileName.encode('utf-8'), server_address)


        filename=("Cliente"+str(client_id)+"-Prueba-"+str(hilos))


        # Recibir los fragmentos del archivo del servidor y guardarlos en un archivo local
        with open(os.path.join(directory,filename ), 'wt') as f:
            start_time = datetime.now()
            while True:
                fragmento, address  = client_socket.recvfrom(bufferSize)
                if not fragmento:
                    break
                f.write(fragmento)

        # Detener temporizador
        end_time = datetime.now()

        transfer_time = end_time - start_time
        log_message = f'Archivo {filename} recibido correctamente. ' \
                    f'Tamaño: {os.path.getsize(os.path.join(directory, filename))} bytes. ' \
                    f'Tiempo de transferencia: {transfer_time.total_seconds()} segundos.'
        logging.info(log_message)

        print('Archivo recibido correctamente')

    except socket.timeout:
        # Generar el registro del archivo de log en caso de que no se pueda recibir el archivo
        log_message = f'No se pudo recibir el archivo {filename}.'
        logging.info(log_message)



# Numero de clientes prueba
numero_clientes = int(input("Ingrese el número de clientes para la prueba: "))

# Nombre archivo a probar
nombre_archivo_carga = input("Ingrese el nombre del archivo : ")


# Creacion de los hilos
threads = []
for i in range(numero_clientes):
    thread = threading.Thread(target=solicitud, args=(i,nombre_archivo_carga,numero_clientes))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()


#cerrar el socket 
client_socket.close()



"""
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
"""  