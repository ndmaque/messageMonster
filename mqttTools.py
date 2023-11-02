from paho.mqtt import client as mqtt_client
import logging
import time

class MqttTools:

    def __init__(self, config):
        self.conf = {
            'client_id': config['client_id'],
            'broker': config['broker'],
            'port': config['port'],
            'sub_topics': config['sub_topics'],
            'FIRST_RECONNECT_DELAY': 1,
            'RECONNECT_RATE': 2,
            'MAX_RECONNECT_COUNT': 12,
            'MAX_RECONNECT_DELAY': 60,
            'FLAG_EXIT': False
        }
        self.mqttClient = {}

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0 and client.is_connected():
            print('on_connect(): Connected to MQTT Broker {}'.format(self.conf['broker']))
            print('Subscribed to {} Topics :'.format(len(self.conf['sub_topics'])))
            for topic in self.conf['sub_topics']:
                print('\t' + topic[0])
            client.subscribe(self.conf['sub_topics'])
            #print(self.conf['sub_topics'][0][0])
            #print('on_connect(): {} Subscribed to {}'.format(self.conf['broker'], '\n'.join(self.conf['sub_topics'])))
        else:
            print('on_connect(): Failed error code = {}'.format(rc))

    def on_disconnect(self, client, userdata, rc):
        logging.info("Disconnected with result code: %s", rc)
        reconnect_count, reconnect_delay = 0, self.conf['FIRST_RECONNECT_DELAY']
        while reconnect_count < self.conf['MAX_RECONNECT_COUNT']:
            logging.info("Reconnecting in %d seconds...", reconnect_delay)
            time.sleep(reconnect_delay)

            try:
                client.reconnect()
                logging.info("Reconnected successfully!")
                return
            except Exception as err:
                logging.error("%s. Reconnect failed. Retrying...", err)

            reconnect_delay *= self.conf['RECONNECT_RATE']
            reconnect_delay = min(reconnect_delay, self.conf['MAX_RECONNECT_DELAY'])
            reconnect_count += 1
        logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)

        self.conf['FLAG_EXIT'] = True
    
    def connect_mqtt(self):
        print('connect_mqtt(): broker = {}'.format(self.conf['broker']))
        self.mqttClient  = mqtt_client.Client(self.conf['client_id'])
        self.mqttClient.connect(self.conf['broker'], self.conf['port'], keepalive=120)
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.on_disconnect = self.on_disconnect
        return self.mqttClient

    def publish(self, topic, msg):
        result = self.mqttClient.publish(topic, msg)
        status = result[0]
        print('publish() {}: {} = {}'.format('OK' if status == 0 else 'Fail', topic, msg))
        return status 