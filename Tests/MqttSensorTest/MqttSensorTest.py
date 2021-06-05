import paho.mqtt.client as mqtt
import time


def on_message_function(client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode('utf-8'))
    temp, motion = message.split(',')
    print(f'{topic}: Temp = {temp}, Motion = {motion}')


client = mqtt.Client('Raspberry Pi')
client.connect('127.0.0.1', 1883) 
client.subscribe('SensingEvent')
client.on_message = on_message_function
client.loop_start()
 
try:
    while(True):
        time.sleep(1)
except KeyboardInterrupt:
    quit()