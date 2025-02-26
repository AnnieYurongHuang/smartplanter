import streamlit as st
import paho.mqtt.client as mqtt

# MQTT setup
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("smartplanter/user_response")

def on_message(client, userdata, msg):
    if msg.topic == "smartplanter/user_response":
        response = msg.payload.decode()
        st.session_state['response'] = response

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883)
client.loop_start()

st.title('Ask Your Plant Questions')
user_query = st.text_input("Enter your question about plants:")
if st.button("Ask"):
    client.publish("smartplanter/user_query", user_query)
    st.session_state['response'] = "Waiting for response..."

if 'response' in st.session_state:
    st.write("Answer:", st.session_state['response'])

