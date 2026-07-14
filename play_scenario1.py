# Scenario 1: noisy speech, 1 speaker at a time.

import numpy as np
import sounddevice as sd

from speech_selector import get_speech
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

NOISE_SPEAKERS = [9, 10, 11, 12]
NOISE_GAIN = 0.3
PLAY_ORDER = [1, 2, 3, 4, 5, 6, 7, 8]
START_DELAY = 3.0
SPEECH_DURATION = 3.0
GAP = 2.0
END_WAIT = 3.0


def tile_to(x, n):
    if len(x) < n:
        x = np.tile(x, int(np.ceil(n / len(x))))
    return x[:n]


def main():
    clip, speech_file = get_speech(duration=SPEECH_DURATION)
    n_clip = len(clip)

    total = (START_DELAY + len(PLAY_ORDER) * SPEECH_DURATION
             + (len(PLAY_ORDER) - 1) * GAP + END_WAIT)
    total_n = int(total * fs)
    out = np.zeros((total_n, N_CHANNELS_OUT))

    noise_clip, noise_file = get_urban_noise(amplitude=NOISE_GAIN)
    noise = tile_to(noise_clip, total_n)
    for spk in NOISE_SPEAKERS:
        out[:, speaker_to_channel[spk]] = noise
    log_event(__file__, NOISE_SPEAKERS, noise_file, round(total, 1), notes="background noise")

    for i, spk in enumerate(PLAY_ORDER):
        s = int((START_DELAY + i * (SPEECH_DURATION + GAP)) * fs)
        ch = speaker_to_channel[spk]
        out[s:s + n_clip, ch] = clip
        log_event(__file__, spk, speech_file, SPEECH_DURATION)
        print(f"Speech -> speaker {spk} (ch {ch}) at t={s / fs:.1f}s")

    print(f"Playing {total:.0f}s total")
    sd.play(out, samplerate=fs, device=DEVICE_ID)
    sd.wait()
    print("done")


if __name__ == "__main__":
    main()
