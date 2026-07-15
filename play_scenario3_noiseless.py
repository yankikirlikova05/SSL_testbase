# 3 speakers at a time
# Three random speech chunks played simultaneously from each speaker group,
# 5s each, 5s gap between, 3s tail.

import numpy as np
import sounddevice as sd

from speech_selector import get_speech
from csv_logger import log_event

from session_config import DEVICE_ID, N_CHANNELS_OUT, fs, speaker_to_channel

GROUPS = [(1, 2, 3), (1, 3, 5), (1, 2, 5), (1, 2, 6), (1, 3, 4), (1, 4, 7), (2, 3, 4)]
START_DELAY = 3.0
SPEECH_DURATION = 5.0
GAP = 5.0
END_WAIT = 3.0


def main():
    clip_a, sound_a = get_speech(duration=SPEECH_DURATION)
    clip_b, sound_b = get_speech(duration=SPEECH_DURATION)
    clip_c, sound_c = get_speech(duration=SPEECH_DURATION)
    clips = [clip_a, clip_b, clip_c]
    sounds = [sound_a, sound_b, sound_c]
    n_clip = len(clip_a)

    total = (START_DELAY + len(GROUPS) * SPEECH_DURATION + (len(GROUPS) - 1) * GAP + END_WAIT)
    total_n = int(total * fs)
    out = np.zeros((total_n, N_CHANNELS_OUT))

    for i, group in enumerate(GROUPS):
        s = int((START_DELAY + i * (SPEECH_DURATION + GAP)) * fs)
        for spk, clip in zip(group, clips):
            out[s:s + n_clip, speaker_to_channel[spk]] = clip
        log_event(__file__, list(group), sounds[:len(group)], SPEECH_DURATION)
        print(f"Speech -> speakers {group} at t={s / fs:.1f}s")

    print(f"Playing {total:.0f}s total...")
    sd.play(out, samplerate=fs, device=DEVICE_ID)
    sd.wait()
    print("done")


if __name__ == "__main__":
    main()
