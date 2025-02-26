import paho.mqtt.client as mqtt
import time
import random

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect('localhost', 1883, 60)
    return client

def publish(client):
    while True:
        temperature = random.randint(15, 30)  # Aloe optimal temp ranges roughly from 15°C to 30°C
        humidity = random.randint(40, 80)  # Aloe optimal humidity ranges roughly from 40% to 80%
        client.publish("smartplanter/temperature", temperature)
        client.publish("smartplanter/humidity", humidity)
        print(f"Published temperature {temperature} and humidity {humidity}")
        time.sleep(5)

client = connect_mqtt()
publish(client)
