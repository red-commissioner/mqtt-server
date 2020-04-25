#!/usr/bin/env python
# -*- coding: utf-8 -*
import paho.mqtt.client as mqtt
from helper import gateway_config as config
from requests import post
from ssl import PROTOCOL_TLS


BASE_URL = 'http://127.0.0.1:8000/mqtt'
SERVER, PORT = config['server'], config['port']
username, password = config['username'], config['password']
topic = '#'


def on_connect(client, userdata, flags, rc):
    print(f'connected to {SERVER}:{PORT} with result code {rc}')
    # subscribing here will mean renewed subscription after losing connection
    print(f'About to subscribe to {topic}')
    client.publish("testing", "missatge_test")
    client.subscribe(topic)


def on_message(client, userdata, message):
    post_data = {'topic': message.topic, 'qos': message.qos, 'payload': message.payload}
    url = f'{BASE_URL}/{message.topic}'
    print(f"url is {url} data is {post_data}")


client = mqtt.Client('subscribber', transport='tcp')
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=None,
    tls_version=PROTOCOL_TLS, ciphers=None)
client.username_pw_set(username=username, password=password)
client.connect(SERVER, PORT)
client.loop_forever()
