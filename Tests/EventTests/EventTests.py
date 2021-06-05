import paho.mqtt.client as mqtt

ip_address = '192.168.2.112'
client = mqtt.Client('Mocker')


def connect():
    client.connect(ip_address, 1883)


def temp_error():
    client.publish('TempError', 'Temperature Sensor may have become disconnected')


def temp_error_clear():
    client.publish('TempErrorClear', 'Temperature Sensor is connected')


def sensing_event(temp, motion):
    client.publish('SensingEvent', f'{temp},{motion}')
