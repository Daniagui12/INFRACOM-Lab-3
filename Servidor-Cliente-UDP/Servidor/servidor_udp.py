import datetime
import logging
import os
import socket
import sys
import threading
import time

buffeSize = 65507 
file1 = 'archivo_100MB'
file2 = 'archivo_250MB'
numConexiones = 25


def enviar_archivo(connection, archivo, address):
    # Enviar archivo por fragmentos
    with open(archivo, 'rb') as f:
        data = f.read(buffeSize)
        start_time = time.monotonic()  # Tiempo de inicio del envío
        while data:
            connection.sendto(data, address)
            data = f.read(buffeSize)
        end_time = time.monotonic()  # Tiempo de fin del envío
    
    # Calcular el tiempo total de envío
    tiempo_total = end_time - start_time
    
    # Registrar en el archivo de log los detalles de la conexión
    nombre_archivo = os.path.basename(archivo)
    log_file = time.strftime('%Y-%m-%d-%H-%M-%S-log.txt', time.localtime())
    with open('Logs/' + log_file, 'a') as f:
        f.write(f'Archivo enviado: {nombre_archivo} ({os.path.getsize(archivo)} bytes)\n')
        f.write(f'Tiempo de envío: {tiempo_total:.2f} segundos\n')
        f.write(f'Conexión recibida desde: {address[0]}:{address[1]}\n\n')

def main():
    # Crear el socket UDP y enlazarlo a un puerto específico
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('127.0.0.1', 65432))
    
    # Esperar a recibir conexiones entrantes
    while True:
        address = udp_socket.recvfrom(buffeSize)
        
        # Identificar cual archivo desea el cliente
        file = input("Enter the file number to send (1 for 100MB or 2 for file250MB): ")
        if file == 1:
            solicitud = file1
        elif file == 2:
            solicitud = file2
        
        
        # Crear un thread para enviar el archivo
        archivo = solicitud
        thread = threading.Thread(target=enviar_archivo, args=(udp_socket, archivo, address))
        thread.start()

if __name__ == '__main__':
    if not os.path.exists('Servidor-Cliente-UDP/Servidor/Logs'):
        os.mkdir('Servidor-Cliente-UDP/Servidor/Logs')
    main()