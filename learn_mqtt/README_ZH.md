# 使用 Paho Python 连接到 GeekOpen 物联网设备
本文主要介绍如何在 Python 项目中使用 paho-mqtt 客户端库 ，实现 GeekOpen 设备与 MQTT 服务器的连接、订阅、收发消息等功能。

paho-mqtt 是目前 Python 中使用较多的 MQTT 客户端库， 它在 Python 2.7.9+ 或 3.6+ 上为客户端类提供了对 MQTT v5.0，v3.1 和 v3.1.1 的支持。它还提供了一些帮助程序功能，使将消息发布到 MQTT 服务器变得非常简单。

## 前提条件

### 安装依赖包

```bash
sudo apt install python3 python3-pip -y
python3 -m pip install paho-mqtt
```


## 连接

### 连接设置

本文将使用 GeekOpen  [物联网平台](http://manage.iot.whut-smart.com/) 提供的接入认证方式，服务器接入信息如下：

- Broker: **mqtt.geek-smart.cn**
- TCP Port: **1883**
- WebSocket Port: **8083**

### 导入依赖包
```python
from paho.mqtt import client as mqtt_client
```
### 定义连接地址、认证信息以及消息发布主题
设置 MQTT Broker 连接地址，端口以及 topic。
```python
BROKER = 'mqtt.geek-smart.cn'
PORT = 1883
PUB_TOPIC = "/HYUGHV/lVtAcHuor***/4cebd60bf***/publish"
SUB_TOPIC = "/HYUGHV/lVtAcHuor***/4cebd60bf***/subscribe"
CLIENT_ID = f'python-mqtt-tcp-client'
USERNAME = '************'
PASSWORD = '************'
```

### 定义消息发布函数

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
### 定义 on_message 回调函数，用于打印订阅主题接收的消息内容
```python
def on_message(client, userdata, msg):
    print(f'Received `{msg.payload.decode()}` from `{msg.topic}` topic')

```

### 初始化 MQTT 客户端并订阅主题
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
### 完整代码
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

## 测试验证
```bash
python3 pub_sub_tcp.py
``` 
![Alt text](./images/res.png)