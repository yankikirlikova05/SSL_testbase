
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

GROUPS = [(1, 2, 3), (1, 3, 5), (1, 2, 5), (1, 2, 6), (1, 3, 4), (1, 4, 7), (2, 3, 4)]
START_DELAY = 1.0
GAP = 3.0
END_WAIT = 2.0


def tile_to(x, n):
    if len(x) < n:
        x = np.tile(x, int(np.ceil(n / len(x))))
    return x[:n]


def main():
    source_amplitude = db_to_amp(SOURCE_GAIN)
    speeches = get_speech(num=3, amplitude=source_amplitude) 
    clips = [clip for clip, _ in speeches]
    sounds = [name for _, name in speeches]
    slot_dur = max(len(c) for c in clips) / fs  # longest of the trio, no crop

    total = (START_DELAY + len(GROUPS) * slot_dur + (len(GROUPS) - 1) * GAP + END_WAIT)
    total_n = int(total * fs)
    out = np.zeros((total_n, N_CHANNELS_OUT))

    noise_amplitude = db_to_amp(NOISE_GAIN)
    noise_files = []
    for spk in NOISE_SPEAKERS:                     # independent random clip per speaker
        noise_clip, noise_file = get_urban_noise(amplitude=noise_amplitude)
        out[:, speaker_to_channel[spk]] = tile_to(noise_clip, total_n)
        noise_files.append(noise_file)
    log_event(__file__, NOISE_SPEAKERS, noise_files, round(total, 1), notes="background noise")

    for i, group in enumerate(GROUPS):
        s = int((START_DELAY + i * (slot_dur + GAP)) * fs)
        for spk, clip in zip(group, clips):
            out[s:s + len(clip), speaker_to_channel[spk]] = clip
        log_event(__file__, list(group), sounds[:len(group)], round(slot_dur, 1))
        print(f"Speech -> speakers {group} at t={s / fs:.1f}s")

    print(f"Playing {total:.0f}s total...")
    sd.play(out, samplerate=fs, device=DEVICE_ID)
    sd.wait()
    print("done")


if __name__ == "__main__":
    main()
