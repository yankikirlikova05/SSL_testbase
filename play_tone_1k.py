#Play a 1 kHz tone from speakers 7, 8, 1, 2, 3 in order.

import time

import numpy as np
import sounddevice as sd

DEVICE_ID = 4
N_CHANNELS_OUT = 16
fs = 48000

speaker_to_channel = {
    1: 11,
    2: 8,
    3: 12,
    4: 15,
    5: 4,
    6: 3,
    7: 1,
    8: 0,
}

FREQ = 1000  
AMPLITUDE = 0.3
TONE_DURATION = 3.0
GAP = 3.0 
START_DELAY = 10.0
PLAY_ORDER = [7, 8, 1, 2, 3]

t = np.linspace(0, TONE_DURATION, int(fs * TONE_DURATION), endpoint=False)
tone = AMPLITUDE * np.sin(2 * np.pi * FREQ * t)

fade_len = int(0.005 * fs)
fade = np.linspace(0.0, 1.0, fade_len)
tone[:fade_len] *= fade
tone[-fade_len:] *= fade[::-1]


def main():
    time.sleep(START_DELAY)

    for spk in enumerate(PLAY_ORDER):
        ch = speaker_to_channel[spk]
        output_signal = np.zeros((len(tone), N_CHANNELS_OUT))
        output_signal[:, ch] = tone

        print(f"Playing {FREQ} Hz from speaker {spk} (channel {ch})...")
        sd.play(output_signal, samplerate=fs, device=DEVICE_ID)
        sd.wait()
       
        time.sleep(GAP)

    print("Done.")


if __name__ == "__main__":
    main()
