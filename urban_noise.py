# Play one random 5s urban noise clip from speakers 9-12.

import numpy as np
import sounddevice as sd

from urban_noise_selector import get_urban_noise
from csv_logger import log_event
from session_config import (
    DEVICE_ID, N_CHANNELS_OUT, fs, speaker_to_channel,
    NOISE_SPEAKERS, NOISE_GAIN,
)

DURATION = 5.0


def main():
    clip, noise_file = get_urban_noise(duration=DURATION, amplitude=NOISE_GAIN)

    out = np.zeros((len(clip), N_CHANNELS_OUT))
    for spk in NOISE_SPEAKERS:
        out[:, speaker_to_channel[spk]] = clip

    log_event(__file__, NOISE_SPEAKERS, noise_file, DURATION, notes="urban noise")
    print(f"Playing urban noise from speakers {NOISE_SPEAKERS} for {DURATION:.0f}s...")
    sd.play(out, samplerate=fs, device=DEVICE_ID)
    sd.wait()
    print("done")


if __name__ == "__main__":
    main()
