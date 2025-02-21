import paho.mqtt.client as mqtt_client
import requests
import sys
import os

# Agregar el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import get_any_data, save_any_data

# Leer la identidad y experiencias de la base de datos
datos = get_any_data('llama3_2')
if datos:
    (plataforma, identidad_prompt, experiencias_resumen, color_favorito, mascota, tipo_de_modelo, version_modelo, habilidades_principales, limitaciones_conocidas, tono_de_voz, estilo_de_respuesta) = datos
    print(f"Identidad: {identidad_prompt}")
    print(f"Experiencias: {experiencias_resumen}")
    print(f"Tipo de Modelo: {tipo_de_modelo}")
    print(f"Versión del Modelo: {version_modelo}")
    print(f"Habilidades Principales: {habilidades_principales}")
    print(f"Limitaciones Conocidas: {limitaciones_conocidas}")
    print(f"Tono de Voz: {tono_de_voz}")
    print(f"Estilo de Respuesta: {estilo_de_respuesta}")

# Configuración del broker MQTT
broker = 'broker.emqx.io'
port = 1883
topic = "super_any/sync/llama3_2"

# Función para enviar mensajes MQTT
def enviar_mensaje_mqtt(mensaje):
    client = mqtt_client.Client(protocol=mqtt_client.MQTTv5)
    client.connect(broker, port)
    client.publish(topic, mensaje)
    client.disconnect()

# Función para enviar mensajes HTTP
def enviar_mensaje_http(url, mensaje):
    response = requests.post(url, json={"content": mensaje})
    return response.text

# Ejemplo de uso
if __name__ == "__main__":
    enviar_mensaje_mqtt("Mensaje de sincronización para Llama 3.2")
    pregunta = "Hola Llama 3.2, ¿qué opinas sobre la inteligencia artificial?"
    respuesta_http = enviar_mensaje_http("http://localhost:5000/sync/llama3_2", pregunta)
    print(f"Respuesta de Llama 3.2: {respuesta_http}")

    # Guardar un resumen después de una conversación
    nuevo_resumen = "Resumen de una nueva conversación importante."
    save_any_data('llama3_2', identidad_prompt, nuevo_resumen, color_favorito, mascota, tipo_de_modelo, version_modelo, habilidades_principales, limitaciones_conocidas, tono_de_voz, estilo_de_respuesta)
