import os
import paho.mqtt.client as mqtt
import requests
from dotenv import load_dotenv

# Load API key securely
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"  

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("smartplanter/user_query")

def on_message(client, userdata, msg):
    if msg.topic == "smartplanter/user_query":
        query = msg.payload.decode()
        response = ask_gemini(query)
        client.publish("smartplanter/user_response", response)

def ask_gemini(query):
    headers = {'Authorization': f'Bearer {"GEMINI_API_KEY"}'}
    response = requests.post(GEMINI_API_URL, json={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json().get('answers', [{}])[0].get('answer', 'No answer found.')
    else:
        return "Error in getting response from Gemini."

client = mqtt


