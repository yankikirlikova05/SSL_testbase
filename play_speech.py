# Noiseless speech: wait 3s, then play 4 random 4s speech clips from random speakers
import random
import time

import numpy as np
import sounddevice as sd

from helpers.speech_selector import get_speech
from data.csv_logger import log_event
from session_config import SOURCE_GAIN
from helpers.utils import db_to_amp

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
    9: 13,
    10: 7,
    11: 10,
    12: 5,
}

SPEECH_SPEAKERS = [1, 2, 3, 4, 5, 6, 7, 8]
START_DELAY = 3.0
GAP = 1.0
N_REPEATS = 4


def main():
    time.sleep(START_DELAY)
    source_amplitude = db_to_amp(SOURCE_GAIN)

    for i in range(N_REPEATS):
        spk = random.choice(SPEECH_SPEAKERS)
        ch = speaker_to_channel[spk]
        clip, sound = get_speech(amplitude=source_amplitude)

        out = np.zeros((len(clip), N_CHANNELS_OUT))
        out[:, ch] = clip

        print(f"Speech {i + 1}/{N_REPEATS} -> speaker {spk} (ch {ch})")
        log_event(__file__, spk, sound, round(len(clip) / fs, 1))
        sd.play(out, samplerate=fs, device=DEVICE_ID)
        sd.wait()

        if i < N_REPEATS - 1:
            time.sleep(GAP)

    print("done")


if __name__ == "__main__":
    main()
