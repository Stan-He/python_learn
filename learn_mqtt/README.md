# Connect to the GeekOpen IOT device with Python3
This article mainly introduces how to use `paho-mqtt` in the Python3 project, and implement the connection, subscription, messaging, unsubscribing and other functions between the GeekOpen IOT device and MQTT broker.

paho-mqtt is currently the most used MQTT client library in Python, which provides support for MQTT v5.0, v3.1 and v3.1.1 for client classes on Python 2.7.9+ or 3.6+. It also provides helper features that make publishing messages to MQTT servers very simple.

## Preconditions

### Install dependency packages

```bash
sudo apt install python3 python3-pip -y
python3 -m pip install paho-mqtt
```


## Connection

### Connection settings

This article will use GeekOpen [Internet of Things Platform]（ http://manage.iot.whut-smart.com/ ）The provided access authentication method and server access information are as follows:

- Broker: **mqtt.geek-smart.cn**
- TCP Port: **1883**
- WebSocket Port: **8083**

### Include dependency library
```python
from paho.mqtt import client as mqtt_client
```
### Define connection addresses, authentication information, and message publishing and receiving topic
Set the MQTT Broker connection address, port, and topic.
```python
BROKER = 'mqtt.geek-smart.cn'
PORT = 1883
PUB_TOPIC = "/HYUGHV/lVtAcHuor***/4cebd60bf***/publish"
SUB_TOPIC = "/HYUGHV/lVtAcHuor***/4cebd60bf***/subscribe"
CLIENT_ID = f'python-mqtt-tcp-client'
USERNAME = '************'
PASSWORD = '************'
```

### Define the message publishing function

```python
def publish(client):
    msg_count = 0
    while not FLAG_EXIT:
        msg_dict = {
            'type': 'info'
        }
        msg = json.dumps(msg_dict)
        if not client.is_connected():
            logging.error("publish: MQTT client is not connected!")
            time.sleep(1)
            continue
        result = client.publish(PUB_TOPIC, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f'Send `{msg}` to topic `{PUB_TOPIC}`')
        else:
            print(f'Failed to send message to topic {PUB_TOPIC}')
        msg_count += 1
        time.sleep(1)

```
### Define the on_message callback function to print the content of the messages received by the subscribed topic
```python
def on_message(client, userdata, msg):
    print(f'Received `{msg.payload.decode()}` from `{msg.topic}` topic')

```

### Initialize the MQTT client and subscribe to topic
```python
def on_connect(client, userdata, flags, rc):
    if rc == 0 and client.is_connected():
        print("Connected to MQTT Broker!")
        client.subscribe(SUB_TOPIC)
    else:
        print(f'Failed to connect, return code {rc}')

def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, keepalive=120)
    client.on_disconnect = on_disconnect
    return client
```
### The full code
```python
import json
import logging
import time

from paho.mqtt import client as mqtt_client

BROKER = 'mqtt.geek-smart.cn'
PORT = 1883
PUB_TOPIC = "/HYUGHV/lVtAcHuor***/4cebd60bf***/publish"
SUB_TOPIC = "/HYUGHV/lVtAcHuor***/4cebd60bf***/subscribe"
CLIENT_ID = f'python-mqtt-tcp-client'
USERNAME = '************'
PASSWORD = '************'


FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

FLAG_EXIT = False


def on_connect(client, userdata, flags, rc):
    if rc == 0 and client.is_connected():
        print("Connected to MQTT Broker!")
        client.subscribe(SUB_TOPIC)
    else:
        print(f'Failed to connect, return code {rc}')


def on_disconnect(client, userdata, rc):
    logging.info("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logging.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            logging.info("Reconnected successfully!")
            return
        except Exception as err:
            logging.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)
    global FLAG_EXIT
    FLAG_EXIT = True


def on_message(client, userdata, msg):
    print(f'Received `{msg.payload.decode()}` from `{msg.topic}` topic')


def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, keepalive=120)
    client.on_disconnect = on_disconnect
    return client


def publish(client):
    msg_count = 0
    while not FLAG_EXIT:
        msg_dict = {
            'type': 'info'
        }
        msg = json.dumps(msg_dict)
        if not client.is_connected():
            logging.error("publish: MQTT client is not connected!")
            time.sleep(1)
            continue
        result = client.publish(PUB_TOPIC, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f'Send `{msg}` to topic `{PUB_TOPIC}`')
        else:
            print(f'Failed to send message to topic {PUB_TOPIC}')
        msg_count += 1
        time.sleep(1)


def run():
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    client = connect_mqtt()
    client.loop_start()
    time.sleep(1)
    if client.is_connected():
        publish(client)
    else:
        client.loop_stop()


if __name__ == '__main__':
    run()

```

## Test
```bash
python3 pub_sub_tcp.py
``` 
![Alt text](./images/res.png)