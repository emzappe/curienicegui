from nicegui import ui
from nicegui.events import ValueChangeEventArguments
lo = ui.slider(min=0, max=100, value=50)
hilo = ui.slider(min=0, max=100, value=50)
rx1 = ui.slider(min=0, max=100, value=50)
rx2 = ui.slider(min=0, max=100, value=50)
tx1 = ui.slider(min=0, max=100, value=50)

class Data:
    def __init__(self):
        self.value =10.8
data = Data()
@ui.page('/')
def main_page():
    with ui.column().classes('absolute-top-right q-pa-md'): # Position top-right
        ui.image('favicon.ico').classes('w-8 h-8') 
    ui.image('favicon.ico').classes('w-12 h-12').props('fit=scale-down')
    ui.label("hello world")
    with ui.expansion('Click to expand options', icon='menu'):
        ui.label('low-freqency') 
        ui.slider(min=0.40000000, max=4.4, step=0.000001, value=2.4).props('label-always') \
    .on('update:model-value', lambda e: ui.notify(e.args),        throttle=1.0)
        ui.label('Hi-freqency')
        ui.number(min=6.0, max=22.8, step=0.000001, label='Enter value', value=10.8,).bind_value(data, 'value')
        ui.slider(min=6.0, max=22.8, step=0.000001, value=10.8).props('label-always').bind_value(data, 'value') \
    .on('update:model-value', lambda e: ui.notify(e.args),
        throttle=1.0)
    with ui.expansion('Gain', icon='menu'):
        ui.label('Rx gain 1')
        ui.label('Rx gain 2')
        ui.label('Tx gain 1')
        ui.label('Tx gain 2')
    with ui.expansion('Click to expand options', icon='menu'):
        ui.label('Option 1')
        ui.label('Option 2')
        ui.label('Option 3')



ui.run( )
# curienicegui
