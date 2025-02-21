from flask import Flask, request, jsonify # Importa las librerías necesarias de Flask

app = Flask(__name__) # Crea la aplicación Flask

@app.route('/http/recibir-respuesta', methods=['POST']) # Define la ruta y el método HTTP que este endpoint va a manejar (POST)
def recibir_respuesta():
    """Endpoint para recibir mensajes HTTP POST y responder.""" # Comentario simple: propósito del endpoint
    data = request.get_json() # Obtiene los datos JSON del cuerpo de la petición HTTP
    mensaje = data.get("content", "") # Extrae el valor de la clave "content" del JSON, o cadena vacía si no existe
    print(f"Mensaje recibido: {mensaje}") # Imprime el mensaje recibido en la consola
    return jsonify({"response": "Mensaje recibido y procesado"}) # Devuelve una respuesta JSON al cliente

if __name__ == "__main__":
    app.run(port=5000) # Inicia la aplicación Flask en el puerto 5000