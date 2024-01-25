import socket
import platform
import getpass


def enviar_informacion_al_servidor():
    try:
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Modificar la IP con ipconfig
        host = "192.168.0.11"
        puerto = 456

        clientsocket.connect((host, puerto))
        system_info = f"Sistema: {platform.system()} {platform.release()}, Versión de Python: {platform.python_version()}"
        print(system_info)
        username = getpass.getuser()
        print(f"Nombre de usuario: {username}")
        full_message = f"{system_info}\nUsuario: {username}\n"
        clientsocket.sendall(full_message.encode())

    except Exception as e:
        print(f"Error al conectar al servidor: {e}")

    finally:
        clientsocket.close()


if __name__ == "__main__":
    enviar_informacion_al_servidor()
