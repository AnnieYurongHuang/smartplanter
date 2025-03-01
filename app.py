import streamlit as st
import paho.mqtt.client as mqtt

# MQTT setup
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("smartplanter/user_response")
    client.subscribe("smartplanter/temperature")
    client.subscribe("smartplanter/humidity")

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}")
    if msg.topic == "smartplanter/user_response":
        st.session_state['response'] = msg.payload.decode()
    elif msg.topic == "smartplanter/temperature":
        st.session_state['temperature'] = float(msg.payload.decode())
        update_history('temperature', st.session_state['temperature'])
    elif msg.topic == "smartplanter/humidity":
        st.session_state['humidity'] = float(msg.payload.decode())
        update_history('humidity', st.session_state['humidity'])

def update_history(key, value):
    if key not in st.session_state:
        st.session_state[key] = []
    st.session_state[key].append(value)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883)
client.loop_start()

# Main UI
st.title('Smart Planter Assistant')

tab1, tab2, tab3 = st.tabs(["Chatbot", "Conditions History", "Plant Status"])

with tab1:
    st.header("Ask About Plant Care")
    query = st.text_input("What is going on with your plant today?")
    if st.button("Submit"):
        client.publish("smartplanter/user_query", query)
        st.session_state['response'] = "Waiting for response..."
    
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
    if 'temperature' in st.session_state and 'humidity' in st.session_state:
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




