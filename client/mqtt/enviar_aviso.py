import paho.mqtt.client as mqtt

broker = 'broker.emqx.io'
port = 1883
topic = "super_any/sync/test"

def enviar_aviso():
    client = mqtt.Client()
    client.connect(broker, port)
    client.publish(topic, "Mensaje de prueba MQTT")
    client.disconnect()

if __name__ == "__main__":
    enviar_aviso()
