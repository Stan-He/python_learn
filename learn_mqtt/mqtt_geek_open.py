import json
import logging
import time

from paho.mqtt import client as mqtt_client

BROKER = ''
PORT = 1883
PUB_TOPIC = "my_topic/publish"
SUB_TOPIC = "my_topic/subscribe"
PUB_TOPIC = "geek_pdu4/publish"
SUB_TOPIC = "geek_pdu4/subscribe"

CLIENT_ID = f'python_mqtt_tcp_client' #mqttx_f2d6e399
USERNAME = 'mh'
PASSWORD = ''



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
    """链接mqtt服务器


    Returns:
        _type_: _description_
    """
    #client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1,CLIENT_ID)
    client = mqtt_client.Client()
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect  #链接成功后，立即订阅指定的topic
    client.on_message = on_message  #接受到消息后，打印消息内容
    client.connect(BROKER, PORT, keepalive=120)
    client.on_disconnect = on_disconnect
    return client


def publish(client):
    msg_count = 0
    loop=0
    while not FLAG_EXIT:
        # msg_dict = {
        #     'type': 'info'
        # }
        msg_dict = {
            'type': 'event',
            'key': loop%2
        }
        loop+=1
        msg = json.dumps(msg_dict)
        if not client.is_connected():
            logging.error("publish: MQTT client is not connected!")
            time.sleep(1)
            continue
        result = client.publish(PUB_TOPIC, msg) #向发布地址发送消息
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f'Send `{msg}` to topic `{PUB_TOPIC}`')
        else:
            print(f'Failed to send message to topic {PUB_TOPIC}')
        msg_count += 1
        time.sleep(2)


def run():
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    client = connect_mqtt() #链接mqtt服务器 注册on_connect、on_message、on_disconnect三个回调函数
    client.loop_start()
    time.sleep(1)
    if client.is_connected():
        publish(client)
    else:
        client.loop_stop()


if __name__ == '__main__':
    #问题1 是否需要使用已经配置过的client id mqttx_f2d6e399？

    run()