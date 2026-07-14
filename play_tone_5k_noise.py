# Play a 5 kHz tone from speakers 7,8,1,2,3 with urban background noise from 9,10,11,12.

import time

import numpy as np
import sounddevice as sd

from urban_noise_selector import get_urban_noise
from csv_logger import log_event

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
AMPLITUDE = 0.3
NOISE_GAIN = 0.3
TONE_DURATION = 3.0
GAP = 3.0
START_DELAY = 10.0
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
    step = len(tone) + int(GAP * fs)
    seq_len = len(PLAY_ORDER) * step
    out = np.zeros((seq_len, N_CHANNELS_OUT))

    noise_clip, noise_file = get_urban_noise(amplitude=NOISE_GAIN)
    noise = tile_to(noise_clip, seq_len)
    for spk in NOISE_SPEAKERS:
        out[:, speaker_to_channel[spk]] = noise
    log_event(__file__, NOISE_SPEAKERS, noise_file, round(seq_len / fs, 1), notes="background noise")

    for i, spk in enumerate(PLAY_ORDER):
        s = i * step
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
