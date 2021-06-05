from time import time
import paho.mqtt.client as mqtt


def decode(data):
    temp, motion = str(data.payload.decode('utf-8')).split(',')
    if temp == '': temp = None
    else: temp = float(temp)
    motion = True if motion == '1' else False
    return temp, motion


class Mqtt:
    _client = None
    _sensing_event_func = None
    _temp_error_func = None
    _temp_error_clear_func = None
    
    _expected_event_interval = 60
    _expected_event_interval_tolerance = 10
    _last_event_time = None
    
    _sensing_event_name = 'SensingEvent'
    _temp_error_name = 'TempError'
    _temp_error_clear_name = 'TempErrorClear'

    def __init__(self, sensing_event_func, temp_error_func, temp_error_clear_func):
        self.client = mqtt.Client('Raspberry Pi')
        self.client.connect('127.0.0.1', 1883)
        self.client.subscribe(self._sensing_event_name)
        self.client.subscribe(self._temp_error_name)
        self.client.subscribe(self._temp_error_clear_name)
        self.client.on_message = self.event_function
        self.client.loop_start()
        self._sensing_event_func = sensing_event_func
        self._temp_error_func = temp_error_func
        self._temp_error_clear_func = temp_error_clear_func
        self._last_event_time = time()


    def event_is_late(self):
        allowance = self._expected_event_interval + self._expected_event_interval_tolerance
        return time() > self._last_event_time + allowance


    def event_function(self, client, userdata, message):
        self._last_event_time = time()
        event = str(message.topic)
        if event == self._sensing_event_name:
            temp, motion = decode(message)
            self._sensing_event_func(temp, motion)
        elif event == self._temp_error_name:
            self._temp_error_func()
        elif event == self._temp_error_clear_name:
            self._temp_error_clear_func()
