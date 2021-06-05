import requests

key = 'IFTTT_KEY_HERE'

mqtt_error_str = 'Lost connection to Sensing Module. Application has turned off heater and ceded control until connection is reestablished.'
temp_error_str = 'Temperature sensor malfunctioning. Application has turned off heater and ceded control until this is fixed.'


def url(event):
    return f'https://maker.ifttt.com/trigger/{event}/with/key/{key}'


def turn_on():
    response = requests.get(url('Turn On Heater'))
    print(response.content)


def turn_off():
    response = requests.get(url('Turn Off Heater'))
    print(response.content)


def temp_error():
    response = requests.post(url('Heating System Error'), { 'value1' : temp_error_str })
    print(response.content)


def mqtt_error():
    response = requests.post(url('Heating System Error'), { 'value1' : mqtt_error_str })
    print(response.content)