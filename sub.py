import paho.mqtt.client as mqtt
import requests
import time
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variables
API_KEY = os.getenv('GEMINI_API_KEY')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("smartplanter/temperature")
    client.subscribe("smartplanter/humidity")

def on_message(client, userdata, msg):
    if msg.topic == "smartplanter/temperature":
        temp = msg.payload.decode()
        print(f"Received temperature {temp}")
    if msg.topic == "smartplanter/humidity":
        humidity = msg.payload.decode()
        print(f"Received humidity {humidity}")
    # Create a prompt from the MQTT message
    # prompt = f"Explain: {msg.payload.decode()}"
    # # Call Gemini API
    # response = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}", json={
    #     "contents": [{
    #     "parts":[{"text": prompt}]
    #     }]})
    # # Print response
    # response_data = json.loads(response.text)
    # text_response = response_data['candidates'][0]['content']['parts'][0]['text']
    # print("Gemini Response:", text_response)

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)  # Connect to MQTT broker

    # Start the subscriber loop
    client.loop_start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping subscriber...")
        client.loop_stop()
        client.disconnect()
