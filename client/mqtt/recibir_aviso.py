import paho.mqtt.client as mqtt

broker = 'broker.emqx.io'
port = 1883
topic = "super_any/sync/test"

def on_message(client, userdata, message):
    print(f"Mensaje recibido: {message.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message
client.connect(broker, port)
client.subscribe(topic)
client.loop_start()

# Esperar indefinidamente
while True:
    pass
