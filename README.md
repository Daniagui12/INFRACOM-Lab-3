# Redes-Lab-3

### Generalidades

* Es necesario instalar una libreria para el uso del programa. Adicionalmente, se requiere acceso a internet para descargar los archivos de prueba necesarios. Para esto se realiza el siguiente proceso.
* Ambos servidores y clientes se encuentran en este repositorio
* Cada Servidor-Cliente tiene su propia carpeta logs, ubicadas en **Servidor-Cliente-XXX/Cliente/Logs** o **Servidor-Cliente-XXX/Servidor/Logs**

### Requisitos

* Instalar python 3.8, para esto usamos el siguiente comando:

```bash
$ apt install python3.8 -y
```

* Instalar la siguiente libreria para la descarga de archivos subidos en Google Drive para las pruebas de los servidores

```bash
$ pip install gdown
```

### Instalación

* Antes de iniciar, es necesario ubicarnos en la carpeta del proyecto

```bash
$ cd INFRACOM-Lab-3
```

* Antes de la ejecución de cada servidor y cliente es necesario ejecutar el siguiente script que se encarga de descargar los archivos de una carpeta en drive

```bash
$ python3.8 files/file_download.py
```

### Ejecución (TCP)

* Para el servidor, se debe ejecutar este de la siguiente forma con el fin de no tener errores con los paths de los archivos usados, esto se hace desde la carpeta base del proyecto.

```bash
$ python3.8 Servidor-Cliente-TCP/Servidor/servidor_tcp_thread.py
```

* Para el cliente, este si debe ejecutarse estando desde su carpeta, de esta forma es necesario ubicarse en esa carpeta primero y luego ejecutar el archivo.

```bash
$ cd Servidor-Cliente-TCP/Cliente
```

```bash
$ python3.8 Cliente/cliente_tcp_thread.py
```
