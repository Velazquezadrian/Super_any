import socket

def start_client():
    # Ruta del socket
    socket_path = '/tmp/super_any_socket'

    # Crear un socket UNIX
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        # Conectarse al servidor
        client_socket.connect(socket_path)

        # Enviar un mensaje al servidor
        message = "Hola desde el cliente"
        client_socket.send(message.encode())

        # Recibir la respuesta del servidor
        response = client_socket.recv(1024).decode()
        print(f"Respuesta del servidor: {response}")

    except socket.error as e:
        print(f"Error en el cliente: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
