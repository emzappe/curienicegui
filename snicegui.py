 
from nicegui import ui
import sys
import rpyc
from pathlib import Path
from nicegui.events import ValueChangeEventArguments
lo = ui.slider(min=0, max=100, value=50)
hilo = ui.slider(min=0, max=100, value=50)
rx1 = ui.slider(min=0, max=100, value=50)
rx2 = ui.slider(min=0, max=100, value=50)
tx1 = ui.slider(min=0, max=100, value=50)
class RadioController:
    def __init__(self):
        self.conn = rpyc.connect('localhost', 37000)
   

    @property
    def srv(self):
        try:
            self.conn.root.keep_alive()
        except Exception:
             self.conn = rpyc.connect('localhost', 37000)
        return self.conn.root

    def update_freq(self, lo, freq):
        freq = float(freq)	
        print(f"Updating frequency for {lo} to {freq}...")
        if lo == "lo":
            self.srv.set_low_LO(freq * 1e9)
        elif lo == "hi":
            self.srv.set_high_LO(freq * 1e9)
        
    
    def update_gain(self, channel, gain):
        gain = int(float(gain))
        print(f"Updating gain for {channel} to {gain}...")
        self.srv.set_gain(channel[:2], int(channel[2]), gain)

    def update_filter(self, channel, v):
    	print(f"Updating filter for {channel} to {v}...")
    	self.srv.set_filter(channel[:2], int(channel[2]), v)
        
    def update_bias(self, channel, iq, v):
    	print(f"Updating bias for TX{channel} {iq} to {v}...")
    	self.srv.set_mixer_bias(channel, iq, v)

    def update_gpio(self, channel, v):
    	print(f"Updating GPIO {channel} to {v}...")
    	self.srv.set_gpio(channel, v)
    def reset_lmx(self):
    	self.srv.reset_lmx()
class Data:
	def __init__(self):
        	self.lowfreq = 2.4
       		self.hifreq = 10.8
        	self.Rx1 = 30
        	self.Rx2 = 30
        	self.Tx1 = 30
		

radio = RadioController()
data = Data()
@ui.page('/')
def main_page():
    with ui.column().classes('absolute-top-right q-pa-md'): # Position top-right
        ui.image('favicon.png').classes('w-8 h-8').props('fit=scale-down') 
    ui.image('favicon.png').classes('w-12 h-12').props('fit=scale-down')
    ui.label("hello world")
    with ui.expansion('Lo', icon='menu'):
        ui.label('low-freqency') 
        ui.number(min=0.4, max=4.4, step=0.000001, label='Enter value', value=0,).bind_value(data, 'lowfreq')\
    .on('update:model-value', lambda e: radio.update_freq('lo', e.args))
        ui.slider(min=0.4, max=4.4, step=0.000001, value=2.4).props('label-always').bind_value(data, 'lowfreq') \
    .on('update:model-value', lambda e: radio.update_freq('lo', e.args),
        throttle=0.5)
        ui.label('Hi-freqency')
        ui.number(min=6.0, max=22.8, step=0.000001, label='Enter value', value=radio.srv.get_high_LO()/1e9,).bind_value(data, 'hifreq')\
    .on('update:model-value', lambda e: radio.update_freq('hi', e.args))
        ui.slider(min=6.0, max=22.8, step=0.000001, value=10.8).props('label-always').bind_value(data, 'hifreq')\
    .on('update:model-value', lambda e: radio.update_freq('hi', e.args),
        throttle=0.5)
        
    with ui.expansion('Gain', icon='menu'):
        ui.label('Rx gain 1')
        ui.number(min=0, max=60, step=0.1, label='Enter value',).bind_value(data, 'Rx1') \
    .on('update:model-value', lambda e: radio.update_gain('rx0', e.args)) 
        ui.slider(min=0, max=60, step=0.1, value=30).props('label-always').bind_value(data, 'Rx1') \
    .on('update:model-value', lambda e: radio.update_gain('rx1', e.args),
        throttle=0.5)
        ui.label('Rx gain 2')
        ui.number(min=0, max=60, step=0.1, label='Enter value',).bind_value(data, 'Rx2')\
    .on('update:model-value', lambda e: radio.update_gain('rx1', e.args))
        ui.slider(min=0, max=60, step=0.1, value=30).props('label-always').bind_value(data, 'Rx2') \
    .on('update:model-value', lambda e: radio.update_gain('rx1', e.args),
        throttle=0.5)
        ui.label('Tx gain 1')
        ui.number(min=0, max=60, step=0.1, label='Enter value',).bind_value(data, 'Tx1')\
    .on('update:model-value', lambda e: radio.update_gain('tx0', e.args))
        ui.slider(min=0, max=60, step=0.1, value=30).props('label-always').bind_value(data, 'Tx1') \
    .on('update:model-value', lambda e: radio.update_gain('tx0', e.args),
        throttle=0.5)

        ui.label('Tx gain 2')
        ui.number(min=0, max=60, step=0.1, label='Enter value',).bind_value(data, 'Tx2')\
    .on('update:model-value', lambda e: radio.update_gain('tx1', e.args))
        ui.slider(min=0, max=60, step=0.1, value=30).props('label-always').bind_value(data, 'Tx2') \
    .on('update:model-value', lambda e: radio.update_gain('tx1', e.args),
        throttle=0.5)

    with ui.expansion('Filters', icon='menu'):
        ui.label('Option 1')
        ui.label('Option 2')
        ui.label('Option 3')


ui.run(
    port=443
)

