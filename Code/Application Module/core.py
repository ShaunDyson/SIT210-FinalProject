from time import time
from datetime import datetime, timedelta

_last_motion = None
_target_temp = 20.0
_target_temp_min = 10.0
_target_temp_max = 30.0
_target_temp_tolerance = 0.5

_inactivity_mins = 60
_inactivity_mins_min = 1
_inactivity_mins_max = 999

_schedule_start = (23,  30)
_schedule_end = (8,  00)

temp = None
control_enabled = False
inactivity_enabled = False
schedule_enabled = False


def mins_since_motion():
    if _last_motion == None: return None
    return (int(time()) - _last_motion) // 60


def motion_detected():
    global _last_motion
    _last_motion = int(time())


def get_schedule_start():
    return _schedule_start


def get_schedule_end():
    return _schedule_end


def valid_time(hr, minute):
    return 0 <= hr <= 23 and 0 <= minute <= 59


def set_schedule(start_hr, start_min, end_hr, end_min):
    global _schedule_start, _schedule_end
    if not valid_time(start_hr, start_min) or not valid_time(end_hr, end_min):
        raise ValueError('Hour must be between 0 and 23. Minute must be between 0 and 59')
    _schedule_start = (start_hr, start_min)
    _schedule_end = (end_hr, end_min)


def set_target_temp(target):
    global _target_temp
    if _target_temp_min <= target <= _target_temp_max: _target_temp = target
    else: raise ValueError(f'Target Temperature must be between {_target_temp_min}˚C and {_target_temp_max}˚C')


def get_target_temp():
    return _target_temp


def set_inactivity_mins(mins):
    global _inactivity_mins
    if _inactivity_mins_min <= mins <= _inactivity_mins_max: _inactivity_mins = mins
    else: raise ValueError(f'Value must be between {_inactivity_mins_min} and {_inactivity_mins_max}')
    
    
def get_inactivity_mins():
    return _inactivity_mins


def inactivity_time_lapsed():
    if inactivity_enabled:
        mins = mins_since_motion()
        return mins == None or mins >= _inactivity_mins
    return False


def heater_on_temp_based():
    if temp == None: return None
    if temp < _target_temp - _target_temp_tolerance: return True
    if temp > _target_temp + _target_temp_tolerance: return False


def in_schedule():
    if not schedule_enabled: return False
    now = datetime.now()
    start_hr, start_min = _schedule_start
    end_hr, end_min = _schedule_end
    start_time = now.replace(hour = start_hr, minute = start_min, second = 0, microsecond = 0)
    end_time = now.replace(hour = end_hr, minute = end_min, second = 0, microsecond = 0)
    if (start_time > end_time): start_time += timedelta(days = 1)
    return start_time <= now <= end_time    


def heater_on():
    if not control_enabled: return None
    if in_schedule(): return heater_on_temp_based()
    if inactivity_time_lapsed(): return False
    return heater_on_temp_based()