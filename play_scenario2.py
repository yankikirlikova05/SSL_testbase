# Scenario 2: noisy speech, 2 speakers at a time.

import numpy as np
import sounddevice as sd

from helpers.speech_selector import get_speech
from helpers.urban_noise_selector import get_urban_noise
from data.csv_logger import log_event

from session_config import (
    DEVICE_ID, N_CHANNELS_OUT, fs, speaker_to_channel,
    NOISE_SPEAKERS, NOISE_GAIN, SOURCE_GAIN,
)
from helpers.utils import db_to_amp

PAIRS = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (3, 4), (3, 5), (3, 6), (3, 7)]
START_DELAY = 3.0
GAP = 5.0
END_WAIT = 3.0


def tile_to(x, n):
    if len(x) < n:
        x = np.tile(x, int(np.ceil(n / len(x))))
    return x[:n]


def main():
    source_amplitude = db_to_amp(SOURCE_GAIN)
    (clip_a, sound_a), (clip_b, sound_b) = get_speech(num=2, amplitude=source_amplitude)
    slot_dur = max(len(clip_a), len(clip_b)) / fs  # longest of the pair, no crop

    total = (START_DELAY + len(PAIRS) * slot_dur + (len(PAIRS) - 1) * GAP + END_WAIT)
    total_n = int(total * fs)
    out = np.zeros((total_n, N_CHANNELS_OUT))

    noise_amplitude = db_to_amp(NOISE_GAIN)
    noise_files = []
    for spk in NOISE_SPEAKERS: 
        noise_clip, noise_file = get_urban_noise(amplitude=noise_amplitude)
        out[:, speaker_to_channel[spk]] = tile_to(noise_clip, total_n)
        noise_files.append(noise_file)
    log_event(__file__, NOISE_SPEAKERS, noise_files, round(total, 1), notes="background noise")

    for i, (a, b) in enumerate(PAIRS):
        s = int((START_DELAY + i * (slot_dur + GAP)) * fs)
        out[s:s + len(clip_a), speaker_to_channel[a]] = clip_a
        out[s:s + len(clip_b), speaker_to_channel[b]] = clip_b
        log_event(__file__, [a, b], [sound_a, sound_b], round(slot_dur, 1))
        print(f"Speech -> speakers {a},{b} at t={s / fs:.1f}s")

    print(f"Playing {total:.0f}s total...")
    sd.play(out, samplerate=fs, device=DEVICE_ID)
    sd.wait()
    print("done")


if __name__ == "__main__":
    main()
