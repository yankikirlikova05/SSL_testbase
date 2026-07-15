# Play one random 5s urban noise clip from speakers 9-12.

import numpy as np
import sounddevice as sd

from helpers.urban_noise_selector import get_urban_noise
from data.csv_logger import log_event
from session_config import (
    DEVICE_ID, N_CHANNELS_OUT, fs, speaker_to_channel,
    NOISE_SPEAKERS, NOISE_GAIN,
)
from helpers.utils import db_to_amp

DURATION = 5.0


def main():
    noise_amplitude = db_to_amp(NOISE_GAIN)
    out = np.zeros((int(DURATION * fs), N_CHANNELS_OUT))
    noise_files = []
    for spk in NOISE_SPEAKERS:                     # independent random clip per speaker
        clip, noise_file = get_urban_noise(duration=DURATION, amplitude=noise_amplitude)
        out[:, speaker_to_channel[spk]] = clip
        noise_files.append(noise_file)

    log_event(__file__, NOISE_SPEAKERS, noise_files, DURATION, notes="urban noise")
    print(f"Playing urban noise from speakers {NOISE_SPEAKERS} for {DURATION:.0f}s...")
    sd.play(out, samplerate=fs, device=DEVICE_ID)
    sd.wait()
    print("done")


if __name__ == "__main__":
    main()
