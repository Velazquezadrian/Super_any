import paho.mqtt.client as mqtt

# Configuración del broker MQTT
broker = 'broker.emqx.io'
port = 1883
topic = "super_any/sync/#"  # El "#" es un comodín para recibir todos los mensajes de subtemas

# Función que se ejecuta cuando nos conectamos al broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT")
        client.subscribe(topic)
    else:
        print(f"Error de conexión: {rc}")

# Función que se ejecuta cuando recibimos un mensaje
def on_message(client, userdata, msg):
    print(f"Mensaje recibido: {msg.payload.decode()} en el topic {msg.topic}")

# Crear un cliente MQTT y configurar las funciones de conexión y mensaje
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Conectar al broker MQTT
client.connect(broker, port, 60)

# Mantener la conexión activa y escuchar mensajes
client.loop_forever()
