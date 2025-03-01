import paho.mqtt.client as mqtt
import time
import random

def connect_mqtt():
    """Create and connect the MQTT client to the broker."""
    client = mqtt.Client("PlantPublisher")
    client.connect("localhost", 1883, 60)
    return client

def publish_sensor_data(client):
    """Publish simulated sensor data at regular intervals."""
    while True:
        temperature = random.uniform(18, 30)  # Aloe Vera thrives between 18°C and 30°C
        humidity = random.uniform(40, 60)     # Ideal humidity for Aloe Vera

        client.publish("smartplanter/temperature", f"{temperature:.2f}")
        client.publish("smartplanter/humidity", f"{humidity:.2f}")

        print(f"Published temperature {temperature:.2f}°C and humidity {humidity:.2f}%")

        time.sleep(10)  # Data updated every 10 seconds for demonstration

if __name__ == "__main__":
    mqtt_client = connect_mqtt()
    publish_sensor_data(mqtt_client)



