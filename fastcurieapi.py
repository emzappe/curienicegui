import sys
import rpyc
from fastapi import FastAPI, Query, HTTPException
from typing import Optional

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Rest API"}

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
      
@app.get("/high_lo")
@app.post("/high_lo")
@app.put("/high_lo")
def high_lo(freq: Optional[float] = Query(None)):
    if freq is not None:
        try:
            radio.update_freq(hi,freq)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to set new frequency {e}")
    return {"frequency": curie.get_high_LO()}



