# Scenario 2 (noiseless): 2 speakers at a time, no background noise.
# Two random speech chunks played simultaneously from each speaker pair,
# 5s each, 5s gap between, 3s tail.

import numpy as np
import sounddevice as sd

from speech_selector import get_speech
from csv_logger import log_event

from session_config import DEVICE_ID, N_CHANNELS_OUT, fs, speaker_to_channel

PAIRS = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (3, 4), (3, 5), (3, 6), (3, 7)]
START_DELAY = 3.0
SPEECH_DURATION = 5.0
GAP = 5.0
END_WAIT = 3.0


def main():
    clip_a, sound_a = get_speech(duration=SPEECH_DURATION)  # two random chunks, reused
    clip_b, sound_b = get_speech(duration=SPEECH_DURATION)
    n_clip = len(clip_a)

    total = (START_DELAY + len(PAIRS) * SPEECH_DURATION + (len(PAIRS) - 1) * GAP + END_WAIT)
    total_n = int(total * fs)
    out = np.zeros((total_n, N_CHANNELS_OUT))

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
