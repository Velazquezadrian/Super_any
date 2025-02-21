import socket
import os

def start_server():
    # Ruta del socket
    socket_path = '/tmp/super_any_socket'

    # Eliminar el socket si ya existe
    if os.path.exists(socket_path):
        os.remove(socket_path)

    try:
        # Configuración del socket del servidor
        server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server_socket.bind(socket_path)
        server_socket.listen(1)
        print("Servidor esperando conexiones...")

        while True:
            client_socket, addr = server_socket.accept()
            print("Conexión establecida")

            try:
                # Recibir mensaje del cliente
                message = client_socket.recv(1024).decode()
                print(f"Mensaje recibido: {message}")

                # Enviar respuesta al cliente
                response = "Mensaje recibido"
                client_socket.send(response.encode())

            except socket.error as e:
                print(f"Error al recibir/enviar datos: {e}")
            finally:
                client_socket.close()

    except socket.error as e:
        print(f"Error en el servidor: {e}")
    finally:
        server_socket.close()
        if os.path.exists(socket_path):
            os.remove(socket_path)

if __name__ == "__main__":
    start_server()
