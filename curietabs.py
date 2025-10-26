
from nicegui import app, ui
import sys
import rpyc
from pathlib import Path
from nicegui.events import ValueChangeEventArguments

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
            print(radio.srv.get_low_LO())
        elif lo == "hi":
            self.srv.set_high_LO(freq * 1e9)
            print(radio.srv.get_high_LO()) 
    
    def update_gain(self, channel, gain):
        gain = int(float(gain))
        print(f"Updating gain for {channel} to {gain}...")
        self.srv.set_gain(channel[:2], int(channel[2]), gain)
        self.print_gains()
    def update_filters(self, channel, v):
        print(f"Updating filter for {channel} to {v}...")
        self.srv.set_filter(channel[:2], int(channel[2]), v)
    def print_gains(self):
        print(radio.srv.get_gain("rx", 0))
        print(radio.srv.get_gain("rx", 1))
        print(radio.srv.get_gain("tx", 0))
        print(radio.srv.get_gain("tx", 1))

    def update_filter(self, channel, v):
    	self.srv.set_filter(channel[:2], int(channel[2]), v['label']) 
    	print(f"Updating filter for {channel} to {v}...")
    	print(radio.srv.get_filter('rx', 0))
    	print(radio.srv.get_filter('rx', 1))
    	print(radio.srv.get_filter('tx', 0))
    	print(radio.srv.get_filter('tx', 1))
    	
 	        
    def update_bias(self, channel, iq, v):
    	v = float(float(v))
    	print(f"Updating bias for TX{channel} {iq} to {v}...")
    	self.srv.set_mixer_bias(channel, iq, v)
    	print(radio.srv.get_mixer_bias(0, 'Q'))
    	print(radio.srv.get_mixer_bias(0, 'I'))
    	print(radio.srv.get_mixer_bias(1, 'Q'))
    	print(radio.srv.get_mixer_bias(1, 'I'))

    	

    def update_gpio(self, channel, v):
    	print(f"Updating GPIO {channel} to {v}...")
    	self.srv.set_gpio(channel, v)
    
    def reset_lmx(self):
    	self.srv.reset_lmx(6, 6)
    	print("reseting lmx")
class Data:
	def __init__(self):
        	self.lowfreq = radio.srv.get_low_LO()/1e9
       		self.hifreq = radio.srv.get_high_LO()/1e9
        	self.Rx1 = radio.srv.get_gain('rx', 0)
        	self.Rx2 = radio.srv.get_gain('rx', 1)
        	self.Tx1 = radio.srv.get_gain('tx', 0)
        	self.Tx2 = radio.srv.get_gain('tx', 1)
        	self.tx0i = radio.srv.get_mixer_bias(0, 'I') 
        	self.tx0q = radio.srv.get_mixer_bias(0, 'Q')
        	self.tx1i = radio.srv.get_mixer_bias(1, 'I')
        	self.tx1q = radio.srv.get_mixer_bias(1, 'Q')
radio = RadioController()
data = Data()
filter_options = {
          "bypass": "bypass", "36MHz": "36MHz", "72MHz": "72MHz", "144MHz": "144MHz",
          "288MHz": "288MHz", "432MHz": "432MHz", "576MHz": "576MHz", "720MHz": "720MHz"
}


@ui.page('/')
def main_page():
    ui.page_title('Curie')
    with ui.header(elevated=True).style('background-color: #DAA420').classes('items-center justify-between'):
        ui.image('favicon.png').classes('w-40 h-20').props('fit=scale-down')
        ui.label('Curie').classes('absolute-center text-black text-3xl')
    with ui.tabs().classes('w-full') as tabs:
        one = ui.tab('Lo & Gains')
        two = ui.tab('Bias')
        three = ui.tab('Filters')
        four = ui.tab('Gpio')
    with ui.tab_panels(tabs, value=one).classes('w-full'):
        with ui.tab_panel(one):
            ui.label('IF freqency') 
            ui.number(min=0.4, max=4.4, step=0.01, label='Enter value', value=0,).bind_value(data, 'lowfreq')\
        .on('update:model-value', lambda e: radio.update_freq('lo', e.args))
            ui.slider(min=0.4, max=4.4, step=0.1, value=2.4).props('label-always').bind_value(data, 'lowfreq') \
        .on('update:model-value', lambda e: radio.update_freq('lo', e.args),
            throttle=0.5)
            ui.label('RF freqency')
            ui.number(min=6.0, max=22.8, step=0.01, label='Enter value', value=radio.srv.get_high_LO()/1e9).bind_value(data, 'hifreq')\
        .on('update:model-value', lambda e: radio.update_freq('hi', e.args))
            ui.slider(min=6.0, max=22.8, step=0.1, value=10.8).props('label-always').bind_value(data, 'hifreq')\
        .on('update:model-value', lambda e: radio.update_freq('hi', e.args),
            throttle=0.5)
            ui.label('Rx gain 1')
            ui.number(min=0, max=60, step=0.1, label='Enter value',).bind_value(data, 'Rx1') \
        .on('update:model-value', lambda e: radio.update_gain('rx0', e.args)) 
            ui.slider(min=0, max=60, step=0.1, value=30).props('label-always').bind_value(data, 'Rx1') \
        .on('update:model-value', lambda e: radio.update_gain('rx0', e.args),
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
        with ui.tab_panel(two):
            ui.label('Tx1 Bias I')
            ui.number(min=-0.4, max=0.4, step=0.001, label='Enter value',).bind_value(data, 'tx0i')\
        .on('update:model-value', lambda e: radio.update_bias(0, "I", e.args))
            ui.slider(min=-0.4, max=0.4, step=0.001, value=0).props('label-always').bind_value(data, 'tx0i') \
        .on('update:model-value', lambda e: radio.update_bias(0, "I", e.args),
            throttle=0.5)
            ui.label('Tx1 Bias Q')
            ui.number(min=-0.4, max=0.4, step=0.001, label='Enter value',).bind_value(data, 'tx0q')\
        .on('update:model-value', lambda e: radio.update_bias(0, "Q", e.args))
            ui.slider(min=-0.4, max=0.4, step=0.001, value=0).props('label-always').bind_value(data, 'tx0q') \
        .on('update:model-value', lambda e: radio.update_bias(0, "Q", e.args),
            throttle=0.5)
            ui.label('Tx2 Bias I')
            ui.number(min=-0.4, max=0.4, step=0.001, label='Enter value',).bind_value(data, 'tx1i')\
        .on('update:model-value', lambda e: radio.update_bias(1, "I", e.args))
            ui.slider(min=-0.4, max=0.4, step=0.001, value=0).props('label-always').bind_value(data, 'tx1i') \
        .on('update:model-value', lambda e: radio.update_bias(1, "I", e.args),
            throttle=0.5)
            ui.label('Tx2 Bias Q')
            ui.number(min=-0.4, max=0.4, step=0.001, label='Enter value',).bind_value(data, 'tx1q')\
        .on('update:model-value', lambda e: radio.update_bias(1, "Q", e.args))
            ui.slider(min=-0.4, max=0.4, step=0.001, value=0).props('label-always').bind_value(data, 'tx1q') \
        .on('update:model-value', lambda e: radio.update_bias(1, "Q", e.args),
            throttle=0.5)

        with ui.tab_panel(four):
            ui.checkbox('Use Internal Reference', value=radio.srv.get_gpio(2), on_change=lambda e: radio.update_gpio(2, e.value))
            ui.checkbox('Use Internal Reference for Low Side', value=radio.srv.get_gpio(3), on_change=lambda e: radio.update_gpio(3, e.value))
            ui.checkbox('Disable Input 20dB Attenuator', value=radio.srv.get_gpio(6), on_change=lambda e: radio.update_gpio(6, e.value))
            ui.button('reset lmx', on_click=lambda: radio.reset_lmx())
        with ui.tab_panel(three):
            rx0_filter =  ui.select(
            options=filter_options, value=radio.srv.get_filter('rx', 0), label='Rx 1 Filter'
       ).on('update:model-value', lambda e: radio.update_filter('rx0', e.args))
            rx1_filter = ui.select(
            options=filter_options, value=radio.srv.get_filter('rx', 1), label='Rx 2 Filter'
       ).on('update:model-value', lambda e: radio.update_filter('rx1', e.args))
            tx0_filter = ui.select(
            options=filter_options, value=radio.srv.get_filter('tx', 0), label='Tx 1 Filter'
       ).on('update:model-value', lambda e: radio.update_filter('tx0', e.args))
            tx1_filter = ui.select(
            options=filter_options, value=radio.srv.get_filter('tx', 1), label='Tx 2 Filter'
       ).on('update:model-value', lambda e: radio.update_filter('tx1', e.args))

@app.get('/freq')
async def freq(lo: str | None = None, freq: float | None = None):
    if lo and freq is not None:
        radio.update_freq(lo, freq)
    return {
        'Low': radio.srv.get_low_LO(),
        'High': radio.srv.get_high_LO()
    }
@app.get('/gain')
async def read_item(chan: str | None = None, val: float | None = None):
    if chan and val is not None:
        radio.update_gain(chan, val)
    return{'TX1': radio.srv.get_gain('tx', 0), 'TX2': radio.srv.get_gain('tx', 1), 'RX1': radio.srv.get_gain('rx', 0), 'RX2': radio.srv.get_gain('rx', 1)}
@app.get('/bias')
async def read_item(chan: int | None = None, iq: str | None = None, val: float | None = None):
    if chan is not None and iq and val is not None:
        radio.update_bias(chan, iq, val)
    return{'TX1 I': radio.srv.get_mixer_bias(0, 'I'), 'TX1 Q': radio.srv.get_mixer_bias(0, 'Q'), 'TX2 I': radio.srv.get_mixer_bias(1, 'I'), 'TX2 Q': radio.srv.get_mixer_bias(1, 'Q')}
@app.get('/filter')
async def read_item(chan:str | None = None, filter: str | None = None):
    if chan and filter is not None:
        radio.update_filters(chan, filter)
    return{'RX1': radio.srv.get_filter('rx', 0), 'RX2': radio.srv.get_filter('rx', 1), 'TX1': radio.srv.get_filter('tx', 0), 'TX2': radio.srv.get_filter('tx', 1) }	
@app.get('/reset')
def resetlmx():
 radio.reset_lmx()
 return "reseting lmx"

ui.run(
    port=443
)
