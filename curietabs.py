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
    	self.srv.set_filter(channel[:2], int(channel[2]), v['label'])
        
    def update_bias(self, channel, iq, v):
    	print(f"Updating bias for TX{channel} {iq} to {v}...")
    	self.srv.set_mixer_bias(channel, iq, v)
    	

    def update_gpio(self, channel, v):
    	print(f"Updating GPIO {channel} to {v}...")
    	self.srv.set_gpio(channel, v)
    
    def reset_lmx(self):
    	self.srv.reset_lmx(6, 6)
    	print("reseting lmx")
class Data:
	def __init__(self):
        	self.lowfreq = 2.4
       		self.hifreq = 10.8
        	self.Rx1 = 30
        	self.Rx2 = 30
        	self.Tx1 = 30
        	self.Tx2 = 30
        	self.tx0i = 0.0 
        	self.tx0q = 0.0
        	self.tx1i = 0.0
        	self.tx1q = 0.0
radio = RadioController()
data = Data()
filter_options = {
          "bypass": "bypass", "36MHz": "36MHz", "72MHz": "72MHz", "144MHz": "144MHz",
          "288MHz": "288MHz", "432MHz": "432MHz", "576MHz": "576MHz", "720MHz": "720MHz"
}


@ui.page('/')
def main_page():     
    with ui.column().classes('absolute-top-right q-pa-md'): # Position top-right
    	ui.image('favicon.png').classes('w-8 h-8').props('fit=scale-down') 
    	ui.image('favicon.png').classes('w-12 h-12').props('fit=scale-down')
    	ui.label("hello world")
    with ui.tabs().classes('w-full') as tabs:
        one = ui.tab('Lo & Gains')
        two = ui.tab('Bias')
        three = ui.tab('Filters')
        four = ui.tab('Gpio')
    with ui.tab_panels(tabs, value=two).classes('w-full'):
        with ui.tab_panel(one):
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
        with ui.tab_panel(two):
            ui.label('Tx0 Bias I')
            ui.number(min=-0.4, max=0.4, step=0.001, label='Enter value',).bind_value(data, 'tx0i')\
        .on('update:model-value', lambda e: radio.update_bias(0, "I", e.args))
            ui.slider(min=-0.4, max=0.4, step=0.001, value=0).props('label-always').bind_value(data, 'tx0i') \
        .on('update:model-value', lambda e: radio.update_bias(0, "I", e.args),
            throttle=0.5)
            ui.label('Tx0 Bias Q')
            ui.number(min=-0.4, max=0.4, step=0.001, label='Enter value',).bind_value(data, 'tx0q')\
        .on('update:model-value', lambda e: radio.update_bias(0, "Q", e.args))
            ui.slider(min=-0.4, max=0.4, step=0.001, value=0).props('label-always').bind_value(data, 'tx0q') \
        .on('update:model-value', lambda e: radio.update_bias(0, "Q", e.args),
            throttle=0.5)
            ui.label('Tx1 Bias I')
            ui.number(min=-0.4, max=0.4, step=0.001, label='Enter value',).bind_value(data, 'tx1i')\
        .on('update:model-value', lambda e: radio.update_bias(1, "I", e.args))
            ui.slider(min=-0.4, max=0.4, step=0.001, value=0).props('label-always').bind_value(data, 'tx1i') \
        .on('update:model-value', lambda e: radio.update_bias(1, "I", e.args),
            throttle=0.5)
            ui.label('Tx1 Bias Q')
            ui.number(min=-0.4, max=0.4, step=0.001, label='Enter value',).bind_value(data, 'tx1q')\
        .on('update:model-value', lambda e: radio.update_bias(1, "Q", e.args))
            ui.slider(min=-0.4, max=0.4, step=0.001, value=0).props('label-always').bind_value(data, 'tx1q') \
        .on('update:model-value', lambda e: radio.update_bias(1, "Q", e.args),
            throttle=0.5)

        with ui.tab_panel(four):
            ui.checkbox('Use Internal Reference', on_change=lambda e: radio.update_gpio(2, e.value))
            ui.checkbox('Use Internal Reference for Low Side', on_change=lambda e: radio.update_gpio(3, e.value))
            ui.checkbox('Disable Input 20dB Attenuator', on_change=lambda e: radio.update_gpio(6, e.value))
            ui.button('reset lmx', on_click=lambda: radio.reset_lmx())
        with ui.tab_panel(three):
            rx0_filter =  ui.select(
            options=filter_options, value="bypass", label='Rx 0 Filter'
       ).on('update:model-value', lambda e: radio.update_filter('rx0', e.args))
            rx1_filter = ui.select(
            options=filter_options, value="bypass", label='Rx 1 Filter'
       ).on('update:model-value', lambda e: radio.update_filter('rx1', e.args))
            tx0_filter = ui.select(
            options=filter_options, value="bypass", label='Tx 0 Filter'
       ).on('update:model-value', lambda e: radio.update_filter('tx0', e.args))
            tx1_filter = ui.select(
            options=filter_options, value="bypass", label='Tx 1 Filter'
       ).on('update:model-value', lambda e: radio.update_filter('tx1', e.args))
@app.get('/freq/{param}/{freq1}')
async def read_item(param, freq1: float):
        radio.update_freq(param, freq1)
        return{'Lo': param, 'Freqency': freq1}
        #return{ 'frequency': curie.get_low_LO() }
        #return{ 'frequency': curie.get_high_LO() }
@app.get('/gain/{chan}/{val}')
async def read_item(chan, val: float):
        radio.update_gain(chan, val)
        return{'channel': chan, 'gain': val}
        #return{'TX0': curie.get_gain('tx', 0), 'TX1': curie.get_gain('tx', 1), 'RX0': curie.get_gain('rx', 0), 'RX1': curie.get_gain('rx', 1)}
@app.get('/bias/{chan}/{iq}/{bval}')
async def read_item(chan: int, iq, bval: float):
        radio.update_bias(chan, iq , bval)
        return{'channel': chan, 'I/Q': iq, 'value': bval}
        #return{'0 I': curie.get_mixer_bias(0, 'I'), '0 Q': curie.get_mixer_bias(0, 'Q'), '1 I': curie.get_mixer_bias(1, 'I'), '1 Q': curie.get_mixer_bias(1, 'Q')}
@app.get('/filter/{chan}/{filter}')
async def read_item(chan, filter: str):
        radio.update_filters(chan, filter)
        return{'channel': chan, 'filter': filter}

  

ui.run(
    port=443
)
