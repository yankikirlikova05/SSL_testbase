import time

import numpy as np
import sounddevice as sd
import soundfile as sf

DEVICE_ID = 4
N_CHANNELS_OUT = 16
fs = 48000
freqs = [220, 300, 350]
duration = 1 # Duration per channel


channel_ids = {
    11 : 1,
    8 : 2,
    12 : 3,
    15 : 4,
    4 : 5,
    3 : 6,
    1 : 7,
    0 : 8,
    13: 9,
    7: 10,
    10: 11,
    5: 12,
   }

t = np.linspace(0, duration, fs*duration)
for channel in channel_ids:
    combined_wave = np.zeros_like(t)
    for freq in freqs:
        sine_wave = 0.3 * np.sin(2 *  np.pi * freq * t)
        combined_wave += sine_wave
    
    output_signal = np.zeros((len(combined_wave), N_CHANNELS_OUT))
    output_signal[:, channel] = combined_wave

    

    sd.play(output_signal, samplerate=fs, device=DEVICE_ID)
    print(channel + output_signal)
    sd.wait()