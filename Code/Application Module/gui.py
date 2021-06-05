import tkinter as tk
from tkinter import font


def get_temp_str(temp):
    return f'{round(temp, 1)}˚C' if temp != None else 'Unknown'


def get_mins_ago_str(mins_ago):
    result = 'Never'
    if mins_ago != None:
        min_mins = 'minute' if mins_ago == 1 else 'minutes'
        result = f'{mins_ago} {min_mins} ago'
    return result


class Gui:
    _closed = False

    _window = None
    _font = None

    _temp_message = None
    _motion_message = None

    _control_enabled = None
    _control_enabled_checkbox = None

    _target_temp_area = None
    _target_temp_message = None
    _target_temp_entry = None
    _target_temp_button = None
    _target_temp_error = None
    _set_target_temp_func = None
    
    _inactivity_area = None
    _inactivity_enabled = None
    _inactivity_checkbox = None
    _inactivity_entry = None
    _inactivity_button = None
    _inactivity_error = None
    _set_inactivity_func = None
    
    _schedule_area = None
    _schedule_enabled = None
    _schedule_checkbox = None
    _schedule_entry = None
    _schedule_button = None
    _schedule_error = None
    _set_schedule_func = None
    
    _general_error_message = None
    

    def __init__(self, set_target_temp_func, set_inactivity_func, set_schedule_func):
        self.create_gui_elements()
        self.pack_gui_elements()
        self._window.title('Heating System')
        self._window.protocol('WM_DELETE_WINDOW', func = self.close)
        self._set_target_temp_func = set_target_temp_func
        self._set_inactivity_func = set_inactivity_func
        self._set_schedule_func = set_schedule_func
    
    
    def get_control_enabled(self):
        return self._control_enabled.get()
    
    
    def get_inactivity_enabled(self):
        return self._inactivity_enabled.get()
    
    
    def get_schedule_enabled(self):
        return self._schedule_enabled.get()
    

    def show_target_temp_error(self, error):
        self._target_temp_error.configure(text = error)
        
        
    def show_inactivity_error(self, error):
        self._inactivity_error.configure(text = error)
        
        
    def show_schedule_error(self, error):
        self._schedule_error.configure(text = error)


    def set_target_temp(self, temp):
        self._target_temp_message.configure(text = f'Target Temperature: {get_temp_str(temp)}')
        
        
    def set_inactivity_mins(self, mins):
        min_mins = 'minute' if mins == 1 else 'minutes'
        self._inactivity_checkbox.configure(text = f'Turn off heater after {mins} {min_mins} of inactivity')
        
        
    def set_schedule(self, start, end):
        self._schedule_checkbox.configure(text = f'Maintain temperature during {start[0]:02d}:{start[1]:02d}-{end[0]:02d}:{end[1]:02d}')
        
        
    def set_general_error(self, error):
        if error != self._general_error_message['text']:
            self._general_error_message.configure(text = error)


    def target_temp_button_func(self):
        text = self._target_temp_entry.get('0.0', tk.END).replace('\n', '')
        try:
            temp = float(text)
            self._set_target_temp_func(temp)
        except ValueError:
            self.show_target_temp_error('Invalid input')
            
            
    def inactivity_button_func(self):
        text = self._inactivity_entry.get('0.0', tk.END).replace('\n', '')
        try:
            mins = int(text)
            self._set_inactivity_func(mins)
        except ValueError:
            self.show_inactivity_error('Invalid input')
            
            
    def schedule_button_func(self):
        text = self._schedule_entry.get('0.0', tk.END).replace('\n','')
        try:
            start, end = text.split('-')
            start_hr, start_min = start.split(':')
            end_hr, end_min = end.split(':')
            start_hr = int(start_hr)
            start_min = int(start_min)
            end_hr = int(end_hr)
            end_min = int(end_min)
            self._set_schedule_func(start_hr, start_min, end_hr, end_min)
        except ValueError:
            self.show_schedule_error('Input must be in the form 00:00-00:00')


    def closed(self):        
        return self._closed


    def update(self, temp, motion_mins_ago):
        temp_str = f'Current Temperature: {get_temp_str(temp)}'
        motion_str = f'Motion last detected: {get_mins_ago_str(motion_mins_ago)}'
        # only update when needed or the text will constantly flicker
        if temp_str != self._temp_message['text']:
            self._temp_message.configure(text = temp_str)
        if motion_str != self._motion_message['text']:
            self._motion_message.configure(text = motion_str)
        self._window.update()


    def pack_target_temp_elements(self):
        self._target_temp_message.pack(side = tk.LEFT, anchor = tk.W)
        tk.Message(self._target_temp_area, width = 10).pack(side = tk.LEFT, anchor = tk.W)
        self._target_temp_entry.pack(side = tk.LEFT, anchor = tk.W)
        self._target_temp_button.pack(side = tk.LEFT, anchor = tk.W)
        self._target_temp_error.pack(anchor = tk.W)


    def create_target_temp_elements(self):
        self._target_temp_area = tk.Frame(self._window)
        self._target_temp_message = tk.Message(self._target_temp_area, font = self._font, width = 250)
        self._target_temp_entry = tk.Text(self._target_temp_area, width = 4, height = 1)
        self._target_temp_button = tk.Button(self._target_temp_area, font = self._font, text = 'Apply', \
            command = self.target_temp_button_func, width = 8, height = 1)
        self._target_temp_error = tk.Message(self._target_temp_area, font = self._font, fg = 'red', width = 250)
    
    
    def pack_inactivity_elements(self):
        self._inactivity_checkbox.pack(side = tk.LEFT, anchor = tk.W)
        tk.Message(self._inactivity_area, width = 10).pack(side = tk.LEFT, anchor = tk.W)
        self._inactivity_entry.pack(side = tk.LEFT, anchor = tk.W)
        self._inactivity_button.pack(side = tk.LEFT, anchor = tk.W)
        self._inactivity_error.pack(side = tk.LEFT, anchor = tk.W)
    
    
    def create_inactivity_elements(self):
        self._inactivity_area = tk.Frame(self._window)
        self._inactivity_enabled = tk.BooleanVar(self._inactivity_area, False)
        self._inactivity_checkbox = tk.Checkbutton(self._inactivity_area, font = self._font, variable = self._inactivity_enabled, \
            onvalue = True, offvalue = False)
        self._inactivity_entry = tk.Text(self._inactivity_area, width = 3, height = 1)
        self._inactivity_button = tk.Button(self._inactivity_area, font = self._font, text = 'Apply', \
            command = self.inactivity_button_func, width = 8, height = 1)
        self._inactivity_error = tk.Message(self._inactivity_area, font = self._font, fg = 'red', width = 250)
    
    
    def pack_schedule_elements(self):
        self._schedule_checkbox.pack(side = tk.LEFT, anchor = tk.W)
        tk.Message(self._schedule_area, width = 10).pack(side = tk.LEFT, anchor = tk.W)
        self._schedule_entry.pack(side = tk.LEFT, anchor = tk.W)
        self._schedule_button.pack(side = tk.LEFT, anchor = tk.W)
        self._schedule_error.pack(side = tk.LEFT, anchor = tk.W)
    

    def create_schedule_elements(self):
        self._schedule_area = tk.Frame(self._window)
        self._schedule_enabled = tk.BooleanVar(self._schedule_area, False)
        self._schedule_checkbox = tk.Checkbutton(self._schedule_area, font = self._font, variable = self._schedule_enabled, \
            onvalue = True, offvalue = False)
        self._schedule_entry = tk.Text(self._schedule_area, width = 11, height = 1)
        self._schedule_button = tk.Button(self._schedule_area, font = self._font, text = 'Apply', \
            command = self.schedule_button_func, width = 8, height = 1)
        self._schedule_error = tk.Message(self._schedule_area, font = self._font, fg = 'red', width = 250)


    def pack_gui_elements(self):
        self._temp_message.pack(anchor = tk.W)
        self._motion_message.pack(anchor = tk.W)
        tk.Message(self._window).pack(anchor = tk.W)
        self._control_enabled_checkbox.pack(anchor = tk.W)
        self._target_temp_area.pack(anchor = tk.W)
        self.pack_target_temp_elements()
        self._inactivity_area.pack(anchor = tk.W)
        self.pack_inactivity_elements()
        self._schedule_area.pack(anchor = tk.W)
        self.pack_schedule_elements()
        self._general_error_message.pack(anchor = tk.W)


    def create_gui_elements(self):
        self._window = tk.Tk()
        self._window.geometry('800x600+100+100')
        self._font = tk.font.Font(family = 'Helvetica', size = 12)
        self._temp_message = tk.Message(self._window, font = self._font, width = 250)
        self._motion_message = tk.Message(self._window, font = self._font, width = 250)
        self._control_enabled = tk.BooleanVar(self._window, True)
        self._control_enabled_checkbox = tk.Checkbutton(self._window, font = self._font, variable = self._control_enabled, \
            onvalue = True, offvalue = False, text = 'Allow application to control heater')
        self.create_target_temp_elements()
        self.create_inactivity_elements()
        self.create_schedule_elements()
        self._general_error_message = tk.Message(self._window, font = self._font, fg = 'red', width = 250)


    def close(self):
        self._closed = True
        self._window.destroy()