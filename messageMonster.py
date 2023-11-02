from datetime import datetime
import time
import random
import logging
import os
import json
from playsound import playsound

# import custom classes
from dataTools import DataTools 
from mqttTools import MqttTools


conf = {
    'client_id': 'ID_NAS_17A_UK',
    'broker': '192.168.0.20',
    'port': 1883,
    'sub_topics': [('status', 0), ('admin/errors', 0), ('admin/commands', 0)],
}

dt = DataTools()
mqtt = MqttTools(conf)

def on_message(client, userdata, msg):
    topic = msg.topic
    message = msg.payload.decode()
    print('on_message(): {} = {}'.format(topic, message)) 

    match topic:
        case 'admin/commands':
            if message == 'SEND_REPORT_A':
                print('Command: {}'.format(message))
            elif message == 'power_off':
                print('Command: {}'.format(message))
                mqtt.publish('alarm', '#FF0000')
            elif message == 'power_on':
                print('Command: {}'.format(message))
                mqtt.publish('alarm', '#00FF00')
            
        case 'admin/errors':
            return "Not found"
        case _:
            print('Topic not found: {}'.format(topic))

def send_stuff(i):
    # colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00']
    # mqtt.publish('alarm', '#FFFF00')
    # mqtt.publish('color', random.choice(colors))
    # mqtt.publish('chart1',  random.randrange(1, 100))
    # mqtt.publish('chart2',  random.randrange(1, 100))
    # mqtt.publish('chart3',  random.randrange(1, 100)) #json.dumps([75, 3, 56, 44]))
    # mqtt.publish('chart4',  random.randrange(1, 100))
    # mqtt.publish('led', 0)
    time.sleep(2)
    # mqtt.publish('led', 1)
    # mqtt.publish('progress', 1 + i)
    # mqtt.publish('progress', 1 + i)
    t = {'stuff': {'cpu': 55+i, 'fan': 357+i , 'disk': '15GB'}}
    #t = {'stuff': [{'cpu': 55+i, 'fan': 357+i , 'disk': '15GB'}, {'cpu': 99+i, 'fan': 8+i , 'disk': '1GB'}]}
    #t = {'stuff': ['aaaa', 'bbbbb', 'ccccc']}
    tmp = json.dumps(t)
    mqtt.publish('alist', tmp)
    mqtt.publish('admin/errors', 'some stuff {}'.format(i))
    mqtt.publish('data/cpu', json.dumps({'data': [{'temp': 25+i, 'fan': 607+i, 'batt': 89+i}, {'temp': 55+i, 'fan': 27+i, 'batt': 9+i}]}))

def main():
    client = mqtt.connect_mqtt()
    client.on_message = on_message
    client.loop_start()
    i = 0
    while True:
        file_path = dt.check_for_new_messages()
        if(file_path):
            msg = dt.get_inbox_message(file_path)
            if(msg):
                mqtt.publish('admin/errors', msg['body'])
            else:
                print('get_inbox_message(): was wonky = {}'.format(msg))

        send_stuff(i)
        time.sleep(5)
        i+=1
     
main()
