import sys
from time import time
import requests
import core
from mqtt import Mqtt
from gui import Gui

mqtt = None
gui = None

heater_last_update_time = 0
heater_update_interval = 30

ifttt_key = 'IFTTT_KEY_HERE'
ifttt_error = 'Heating System Error'
ifttt_on = 'Turn On Heater'
ifttt_off = 'Turn Off Heater'

mqtt_error = False
temp_error = False
internet_error = False

mqtt_error_str = 'Lost connection to Sensing Module. Application has turned off heater and ceded control until connection is reestablished.'
temp_error_str = 'Temperature sensor malfunctioning. Application has turned off heater and ceded control until this is fixed.'
internet_error_str = 'Lost connection to internet.'


def trigger_ifttt(event_name, data):
    global heater_last_update_time, internet_error
    try:
        url = f'https://maker.ifttt.com/trigger/{event_name}/with/key/{ifttt_key}'
        if data == '': requests.get(url)
        else: requests.post(url, { 'value1' : data })
        heater_last_update_time = time()
        internet_error = False
    except:
        internet_error = True
        return


def sensing_event(temp, motion):
    core.temp = temp
    if motion: core.motion_detected()
        
        
def set_general_error():
    error = ''
    if mqtt.event_is_late(): error += f'{mqtt_error_str}\n'
    if temp_error: error += f'{temp_error_str}\n'
    if internet_error: error += f'{internet_error_str}'
    gui.set_general_error(error)


def temp_error_event():
    global temp_error
    temp_error = True
    if core.control_enabled: trigger_ifttt(ifttt_off, '')
    trigger_ifttt(ifttt_error, temp_error_str)


def temp_error_clear_event():
    global temp_error
    temp_error = False


def set_target_temp(temp):
    try:
        core.set_target_temp(temp)
        gui.set_target_temp(core.get_target_temp())
    except ValueError as e:
        gui.show_target_temp_error(str(e))
        return
    gui.show_target_temp_error('')


def set_inactivity_mins(mins):
    try:
        core.set_inactivity_mins(mins)
        gui.set_inactivity_mins(core.get_inactivity_mins())
    except ValueError as e:
        gui.show_inactivity_error(str(e))
        return
    gui.show_inactivity_error('')


def set_schedule(start_hr, start_min, end_hr, end_min):
    try:
        core.set_schedule(start_hr, start_min, end_hr, end_min)
        gui.set_schedule(core.get_schedule_start(), core.get_schedule_end())
    except ValueError as e:
        gui.set_schedule_error(str(e))


def update_heater():
    heater_on = core.heater_on()
    if heater_on == None: return
    if time() > heater_last_update_time + heater_update_interval:
        event_name = ifttt_on if heater_on else ifttt_off
        trigger_ifttt(event_name, '')


def check_mqtt():
    global mqtt_error
    if mqtt.event_is_late():
        if not mqtt_error:
            if core.control_enabled: trigger_ifttt(ifttt_off, '')
            trigger_ifttt(ifttt_error, mqtt_error_str)            
            mqtt_error = True
        return False
    mqtt_error = False
    return True


def loop():
    while True:
        if gui.closed(): return
        core.control_enabled = gui.get_control_enabled()
        core.inactivity_enabled = gui.get_inactivity_enabled()
        core.schedule_enabled = gui.get_schedule_enabled()
        if check_mqtt(): update_heater()
        set_general_error()
        gui.update(core.temp, core.mins_since_motion())


def main():
    global gui, mqtt
    mqtt = Mqtt(sensing_event, temp_error_event, temp_error_clear_event)
    gui = Gui(set_target_temp, set_inactivity_mins, set_schedule)
    gui.set_target_temp(core.get_target_temp())
    gui.set_inactivity_mins(core.get_inactivity_mins())
    gui.set_schedule(core.get_schedule_start(), core.get_schedule_end())
    loop()
    sys.exit()


if __name__ == '__main__':
    main()