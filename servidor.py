import socket
import time

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
puerto = 456
print(host)

serversocket.bind((host, puerto))
serversocket.listen(3)

print("Servidor ejecutándose. Esperando conexiones...")

while True:
    clientsocket, address = serversocket.accept()

    hora_conexion = time.strftime("%Y-%m-%d %H:%M:%S")

    print(f"Recibida conexión desde {address[0]} a las {hora_conexion}")

    data = clientsocket.recv(1024)
    decoded_data = data.decode("utf-8")
    print(f"Datos recibidos {decoded_data}")

    respuesta = (
        f"Hola, te has conectado a las {hora_conexion}".encode("utf-8") + b"\r\n"
    )

    clientsocket.send(respuesta)
    with open("log.txt", "a") as log_file:
        log_file.write(f"Recibida conexión desde {address[0]} a las {hora_conexion}\n")
        log_file.write(f"Datos recibidos: {decoded_data}\n")
        log_file.write("-" * 40 + "\n")
    clientsocket.close()
