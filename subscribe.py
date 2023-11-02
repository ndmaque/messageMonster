from datetime import datetime
import time
import logging
import random
import os
from playsound import playsound
from paho.mqtt import client as mqtt_client

conf = {
    'client_id': f'python-mqtt-tcp-pub-sub-{random.randint(0, 1000)}',
    'broker': '192.168.0.20',
    'port': 1883,
    'topic': 'admin/errors',
    'FIRST_RECONNECT_DELAY': 1,
    'RECONNECT_RATE': 2,
    'MAX_RECONNECT_COUNT': 12,
    'MAX_RECONNECT_DELAY': 60,
    'FLAG_EXIT': False
}

def on_message(client, userdata, msg):
    print(f'Received AAA `{msg.payload.decode()}` from `{msg.topic}` topic')   

def connect_mqtt():
    print(conf['broker'])
    client = mqtt_client.Client(conf['client_id'])
    #client.on_connect = on_connect
    client.on_message = on_message
    client.connect(conf['broker'], conf['port'], keepalive=120)
    #client.on_disconnect = on_disconnect
    return client

def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):
        print(f"Received  `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message

def main():
    client = connect_mqtt()
    subscribe(client, conf['topic'])
    client.loop_forever()
    while True:
        print()

main()