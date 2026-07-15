# Scenario 2: noisy speech, 2 speakers at a time.

import numpy as np
import sounddevice as sd

from speech_selector import get_speech
from urban_noise_selector import get_urban_noise
from csv_logger import log_event

from session_config import (
    DEVICE_ID, N_CHANNELS_OUT, fs, speaker_to_channel,
    NOISE_SPEAKERS, NOISE_GAIN,
)

PAIRS = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (3, 4), (3, 5), (3, 6), (3, 7)]
START_DELAY = 3.0
SPEECH_DURATION = 5.0
GAP = 5.0
END_WAIT = 3.0


def tile_to(x, n):
    if len(x) < n:
        x = np.tile(x, int(np.ceil(n / len(x))))
    return x[:n]


def main():
    clip_a, sound_a = get_speech(duration=SPEECH_DURATION)
    clip_b, sound_b = get_speech(duration=SPEECH_DURATION)
    n_clip = len(clip_a)

    total = (START_DELAY + len(PAIRS) * SPEECH_DURATION + (len(PAIRS) - 1) * GAP + END_WAIT)
    total_n = int(total * fs)
    out = np.zeros((total_n, N_CHANNELS_OUT))

    noise_files = []
    for spk in NOISE_SPEAKERS:                     # independent random clip per speaker
        noise_clip, noise_file = get_urban_noise(amplitude=NOISE_GAIN)
        out[:, speaker_to_channel[spk]] = tile_to(noise_clip, total_n)
        noise_files.append(noise_file)
    log_event(__file__, NOISE_SPEAKERS, noise_files, round(total, 1), notes="background noise")

    for i, (a, b) in enumerate(PAIRS):
        s = int((START_DELAY + i * (SPEECH_DURATION + GAP)) * fs)
        out[s:s + n_clip, speaker_to_channel[a]] = clip_a
        out[s:s + n_clip, speaker_to_channel[b]] = clip_b
        log_event(__file__, [a, b], [sound_a, sound_b], SPEECH_DURATION)
        print(f"Speech -> speakers {a},{b} at t={s / fs:.1f}s")

    print(f"Playing {total:.0f}s total...")
    sd.play(out, samplerate=fs, device=DEVICE_ID)
    sd.wait()
    print("done")


if __name__ == "__main__":
    main()
