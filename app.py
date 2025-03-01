import streamlit as st
import paho.mqtt.client as mqtt
import datetime
from dotenv import load_dotenv
import os
import requests
import json

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variables
API_KEY = os.getenv('GEMINI_API_KEY')

# MQTT setup
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("smartplanter/temperature")
    client.subscribe("smartplanter/humidity")

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}")
    if msg.topic == "smartplanter/temperature":
        temp = float(msg.payload.decode())
        print(f"Received temperature {temp}")
        update_history('temperature', temp)
    elif msg.topic == "smartplanter/humidity":
        humidity = float(msg.payload.decode())
        print(f"Received humidity {humidity}")
        update_history('humidity', humidity)

def update_history(key, value):
    if key not in st.session_state:
        st.session_state[key] = []
    st.session_state[key].append((datetime.datetime.now(), value))
    # # # st.session_state[key] = list(st.session_state[key])
    # # st.session_state[key] = [1.234]
    # st.session_state = {'temperature': 1.234, 'humidity': 4.321}
    print(f"session_state[{key}]: {st.session_state[key]}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_start()

# Main UI
st.title('Smart Planter Assistant')

tab1, tab2, tab3 = st.tabs(["Chatbot", "Conditions History", "Plant Status"])

with tab1:
    st.header("Ask About Plant Care")
    query = st.text_input("What is going on with your plant today?")
    if st.button("Submit"):
        st.session_state['response'] = "Waiting for response..."
        # Create a prompt from the MQTT message
        prompt = f"Explain: {query}"
        # Call Gemini API
        response = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}", json={
            "contents": [{
            "parts":[{"text": prompt}]
            }]})
        # Print response
        response_data = json.loads(response.text)
        text_response = response_data['candidates'][0]['content']['parts'][0]['text']
        print("Gemini Response:", text_response)
        st.session_state['response'] = text_response
    
    if 'response' in st.session_state:
        st.text_area("Response", st.session_state['response'], height=150)

with tab2:
    st.header("Historical Data")
    if 'temperature' in st.session_state:
        st.line_chart(st.session_state['temperature'])
    if 'humidity' in st.session_state:
        st.line_chart(st.session_state['humidity'])

with tab3:
    st.header("Plant Status")
    print('hello world')
    if 'temperature' in st.session_state and 'humidity' in st.session_state:
        print("Updating plant status...")
        # Assuming optimal ranges (you can adjust these ranges)
        optimal_temp = (18, 25)
        optimal_humidity = (40, 60)
        
        last_temp = st.session_state['temperature'][-1]
        last_hum = st.session_state['humidity'][-1]
        
        if optimal_temp[0] <= last_temp <= optimal_temp[1] and optimal_humidity[0] <= last_hum <= optimal_humidity[1]:
            emoji = "😃"  # Happy face for good conditions
            message = "Your plant is doing great!"
        else:
            emoji = "😟"  # Sad face for poor conditions
            message = "Your plant needs attention."
        
        st.markdown(f"### Plant Status: {emoji}")
        st.caption(message)




