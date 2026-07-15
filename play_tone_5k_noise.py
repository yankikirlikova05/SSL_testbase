# Play a 5 kHz tone from speakers 7,8,1,2,3 with urban background noise from 9,10,11,12.

import time

import numpy as np
import sounddevice as sd

from helpers.urban_noise_selector import get_urban_noise
from data.csv_logger import log_event
from helpers.utils import db_to_amp
from session_config import SOURCE_GAIN, NOISE_GAIN

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

FREQ = 5000
AMPLITUDE = db_to_amp(SOURCE_GAIN)
NOISE_GAIN = db_to_amp(NOISE_GAIN)
TONE_DURATION = 3.0
GAP = 3.0
START_DELAY = 10.0
NOISE_LEAD = 3.0   # noise starts, then wait this long before the tone sequence
PLAY_ORDER = [7, 8, 1, 2, 3]
NOISE_SPEAKERS = [9, 10, 11, 12]

t = np.linspace(0, TONE_DURATION, int(fs * TONE_DURATION), endpoint=False)
tone = AMPLITUDE * np.sin(2 * np.pi * FREQ * t)

fade_len = int(0.005 * fs)
fade = np.linspace(0.0, 1.0, fade_len)
tone[:fade_len] *= fade
tone[-fade_len:] *= fade[::-1]


def tile_to(x, n):
    if len(x) < n:
        x = np.tile(x, int(np.ceil(n / len(x))))
    return x[:n]


def main():
    lead_n = int(NOISE_LEAD * fs)
    step = len(tone) + int(GAP * fs)
    seq_len = len(PLAY_ORDER) * step
    total_n = lead_n + seq_len                     # noise runs the whole time; tones start after the lead
    out = np.zeros((total_n, N_CHANNELS_OUT))

    noise_files = []
    for spk in NOISE_SPEAKERS:                     # independent random clip per speaker
        noise_clip, noise_file = get_urban_noise(amplitude=NOISE_GAIN)
        out[:, speaker_to_channel[spk]] = tile_to(noise_clip, total_n)
        noise_files.append(noise_file)
    log_event(__file__, NOISE_SPEAKERS, noise_files, round(total_n / fs, 1), notes="background noise")

    for i, spk in enumerate(PLAY_ORDER):
        s = lead_n + i * step
        ch = speaker_to_channel[spk]
        out[s:s + len(tone), ch] = tone
        log_event(__file__, spk, f"{FREQ}Hz_tone", TONE_DURATION)
        print(f"Tone {FREQ} Hz -> speaker {spk} (ch {ch}) at t={START_DELAY + s / fs:.1f}s")

    time.sleep(START_DELAY)
    sd.play(out, samplerate=fs, device=DEVICE_ID)
    sd.wait()
    print("Done.")


if __name__ == "__main__":
    main()
