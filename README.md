# curienicegui
fastapi calls
/freq?lo=[hi/lo]&freq=[freqency]




/gain?chan=[rx0-1/tx0-1]&val=[0-60]
gain control


/bias?chan=[0-1]&iq=[I/Q]&val=[-0.4_0.4]
bias control



/filter?chan=[rx0-1/tx0-1]&val=[filter_options]
filter control
 filter_options = [
            'bypass', '36MHz', '72MHz', '144MHz',
            '288MHz', '432MHz', '576MHz', '720MHz'
        ]




/reset
resets lmx
