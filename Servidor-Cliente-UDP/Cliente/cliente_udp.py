import os
import time
import socket 
import datetime

#Tamaño maximo de bytes de paquetes UDP
bufferSize = 65535

#Numero de clientes
numClientes = 25

#Puerto y Direccion IP del servidor 
IP= '127.0.0.1'
PUERTO= 65432

#Crear un socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Enviar un mensaje al servidor del archivo a solicitar
fileName =input("Ingrese nombre del archivo ('archivo_100MB' o 'archivo_250MB') ")
client_socket.sendto(fileName.encode('utf-8'), (IP, PUERTO))


inicio_transferencia = datetime.datetime.now()
# Recibir los fragmentos del archivo del servidor y guardarlos en un archivo local
with open('Archivosrecibidos', 'wb') as f:
    while True:
        fragmento, direccion_servidor = client_socket.recvfrom(bufferSize)
        if not fragmento:
            break
        f.write(fragmento)

# Detener temporizador
fin_transferencia = datetime.datetime.now()

# Calcular tiempo transcurrido
tiempo = fin_transferencia - inicio_transferencia

# Obtener información del archivo recibido
nombre_archivo = os.path.basename('Archivosrecibidos')
tamaño_Archivo = os.path.getsize('Archivosrecibidos')


# Escribir registro en un archivo de registro
with open('registro.txt', 'a') as f:
    registro = f'Nombre del archivo :{nombre_archivo}\t Tamaño del archivo{tamaño_Archivo}\t  Total Tiempo{tiempo}\n'
    f.write(registro)


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