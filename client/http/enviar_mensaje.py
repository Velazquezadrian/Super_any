import requests

def enviar_mensaje(mensaje):
    """Envia un mensaje HTTP POST al servidor.""" # Comentario simple: propósito de la función
    url = "http://localhost:5000/http/recibir-respuesta" # URL del endpoint para recibir respuestas HTTP
    response = requests.post(url, json={"content": mensaje}) # Envia el mensaje al servidor como JSON
    print(f"Respuesta del servidor: {response.text}") # Imprime la respuesta del servidor

if __name__ == "__main__":
    enviar_mensaje("Enviar un resumen de la conversación.") # Envia un mensaje de ejemplo
