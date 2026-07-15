# Scenario 2 (noiseless): 2 speakers at a time, no background noise.
# Two random speech chunks played simultaneously from each speaker pair,
# 5s each, 5s gap between, 3s tail.

import numpy as np
import sounddevice as sd

from helpers.speech_selector import get_speech
from data.csv_logger import log_event

from session_config import DEVICE_ID, N_CHANNELS_OUT, fs, speaker_to_channel, SOURCE_GAIN
from helpers.utils import db_to_amp

PAIRS = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (3, 4), (3, 5), (3, 6), (3, 7)]
START_DELAY = 3.0
GAP = 5.0
END_WAIT = 3.0


def main():
    source_amplitude = db_to_amp(SOURCE_GAIN)
    clip_a, sound_a = get_speech(amplitude=source_amplitude)  # two random chunks, reused
    clip_b, sound_b = get_speech(amplitude=source_amplitude)
    slot_dur = max(len(clip_a), len(clip_b)) / fs  # longest of the pair, no crop

    total = (START_DELAY + len(PAIRS) * slot_dur + (len(PAIRS) - 1) * GAP + END_WAIT)
    total_n = int(total * fs)
    out = np.zeros((total_n, N_CHANNELS_OUT))

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
