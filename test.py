#!/usr/bin/env python
# -*- coding: utf-8 -*
import paho.mqtt.client as mqtt
from helper import gateway_config, commissioner_config as config
from requests import post
import ssl


COMMISSIONER_URL = 'http://127.0.0.1:8000/mqtt'
SERVER, COMMISSIONER_PORT = config['server'], config['port']
username, password = config['username'], config['password']
topic = '#'

commissioner_listener = mqtt.Client('middleware', transport='websockets')
gateway_publisher = mqtt.Client('gateway', transport='tcp')

def on_connect(client, userdata, flags, rc):
    print(f'connected to {SERVER} with result code {rc}')
    # subscribing here will mean renewed subscription after losing connection
    client.subscribe(topic)

def on_connect_gateway(client, userdata, flags, rc):
    client.subscribe(topic)

from ipdb import set_trace
def commissioner_on_message(client, userdata, message):
    # set_trace()
    if message.topic.split('/')[0] != 'gw':
        result = gateway_publisher.publish('gw/' + message.topic, message.payload)
        post_data = {'topic': message.topic, 'qos': message.qos, 'payload': message.payload}
        print(f"Message received: {post_data}")
        response = post(f'{COMMISSIONER_URL}/{message.topic}', data=post_data)


def on_connect_gateway(client, userdata, flags, rc):
    print(f'connected with result code {rc}')
    # subscribing here will mean renewed subscription after losing connection
    client.subscribe(topic)
    client.publish("prova", 'test')

def gateway_on_message(client, userdata, message):
    print("You have arrived to the gateway")
    print(f"Message was {message}")
    pass


commissioner_listener.on_connect = on_connect
commissioner_listener.on_message = commissioner_on_message


gateway_publisher.on_connect = on_connect_gateway
gateway_publisher.on_message = gateway_on_message
gateway_publisher.username_pw_set(username=username, password=password)
gateway_publisher.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=None, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
print(f"Trying to connect to {gateway_config}")
gateway_publisher.connect(gateway_config['server'], gateway_config['port'])

commissioner_listener.connect(SERVER, COMMISSIONER_PORT)

commissioner_listener.loop_forever()
