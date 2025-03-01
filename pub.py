import paho.mqtt.client as mqtt
import time
import json
import random
from datetime import datetime

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def log_result(result: mqtt.MQTTMessageInfo):
    # result = client.publish("topic/test", message)  # Publish message to topic
    status = result[0]
    if status == 0:
        print(f"Send `{temperature}` to topic `topic/test`")
    else:
        print(f"Failed to send message to topic due to {status}")

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect

    client.connect("localhost", 1883, 60)  # Connect to the MQTT broker (adjust the IP if needed)
    client.loop_start()  # Start the loop in the background

    try: 
        while True:
            temperature = random.uniform(18, 30)  # Aloe Vera thrives between 18°C and 30°C
            humidity = random.uniform(40, 60)     # Ideal humidity for Aloe Vera

            temp_result = client.publish("smartplanter/temperature", f"{temperature:.2f}")
            humidity_result = client.publish("smartplanter/humidity", f"{humidity:.2f}")
            log_result(temp_result)
            log_result(humidity_result)
            time.sleep(10)

    except KeyboardInterrupt:
        print("Stopping publisher...")
        client.loop_stop()
        client.disconnect()

