#!/usr/bin/env python
# -*- coding: utf-8 -*
import paho.mqtt.client as mqtt
from helper import commissioner_config, gateway_config as config
from time import sleep
from ssl import PROTOCOL_TLS


SERVER, PORT = config['server'], config['port']
username, password = config['username'], config['password']

C_SERVER, C_PORT = commissioner_config['server'], commissioner_config['port']

messages = []

def on_message(client, userdata, message):
    print(f"{client._host}:{client._port}/{message.topic}/p={message.payload} (QoS={message.qos})")
    messages.append((message.topic, message.payload))


def on_connect(client, userdata, flags, rc):
    if not rc:
        print("connected to server")
        client.subscribe('#')
    else:
        print("something went wrong")


c_client = mqtt.Client('commissioner-client', transport='websockets')
c_client.on_connect = on_connect
c_client.on_message = on_message
c_client.connect(C_SERVER, C_PORT)
c_client.loop_start()

client = mqtt.Client('app-publisher', transport='tcp')
client.on_connect = on_connect
client.username_pw_set(username=username, password=password)
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=None,
    tls_version=PROTOCOL_TLS, ciphers=None)
client.connect(SERVER, PORT)
client.loop_start()

try:
    while True:
        
        if messages:
            topic, payload = messages.pop()
            print(f'About to publish on {topic} payload: {payload}')
            res = client.publish(topic, payload)

        sleep(0.4)
except KeyboardInterrupt:
    c_client.disconnect()
    c_client.loop_stop()
    client.disconnect()
    client.loop_stop()

