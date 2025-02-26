import paho.mqtt.client as mqtt

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe inside on_connect to automatically re-subscribe on reconnect
    if rc == 0:
        client.subscribe("your/topic/here")

def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode()}")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# Setup MQTT client and assign event callbacks
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

# Connect and start the loop
client.connect("localhost", 1883, 60)
client.loop_start()
