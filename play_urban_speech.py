# Play urban noise from speakers 9,10,11,12 and speech1.wav from speaker 1

#      find speech recording , timit, libery speech 

import glob
import os
from math import gcd

import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.signal import resample_poly

from helpers.speech_selector import get_speech
from data.csv_logger import log_event
from session_config import SOURCE_GAIN, NOISE_GAIN
from helpers.utils import db_to_amp

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

URBAN_DIR = "urban"
NOISE_SPEAKERS = [9, 10, 11, 12]
SPEECH_SPEAKER = 1

SPEECH_DELAY = 5.0   # noise runs this long before speech starts
NOISE_TAIL = 5.0     # noise keeps running this long after speech ends


def resample_to(x, sr):
    if sr == fs:
        return x
    g = gcd(sr, fs)
    return resample_poly(x, fs // g, sr // g)


def fit_length(x, n):
    if len(x) < n:
        x = np.tile(x, int(np.ceil(n / len(x))))
    return x[:n]


def load_source(path, n_samples, amplitude):
    data, sr = sf.read(path, always_2d=False)
    if data.ndim > 1:
        data = data.mean(axis=1)
    data = data.astype(np.float64)
    data = resample_to(data, sr)
    peak = np.max(np.abs(data))
    if peak > 0:
        data = data / peak * amplitude
    data = fit_length(data, n_samples)
    return data


def main():
    source_amplitude = db_to_amp(SOURCE_GAIN)
    noise_amplitude = db_to_amp(NOISE_GAIN)

    speech, speech_file = get_speech(amplitude=source_amplitude)  # random whole file, no crop
    speech_dur = len(speech) / fs
    total = SPEECH_DELAY + speech_dur + NOISE_TAIL
    total_n = int(total * fs)
    out = np.zeros((total_n, N_CHANNELS_OUT))

    urban_files = sorted(glob.glob(os.path.join(URBAN_DIR, "*.mp3")))
    used_speakers, used_files = [], []
    for spk, f in zip(NOISE_SPEAKERS, urban_files):
        ch = speaker_to_channel[spk]
        out[:, ch] = load_source(f, total_n, noise_amplitude)
        used_speakers.append(spk)
        used_files.append(os.path.basename(f))
        print(f"Noise  speaker {spk} (ch {ch}): {os.path.basename(f)}")
    log_event(__file__, used_speakers, used_files, round(total, 1), notes="background noise")

    start = int(SPEECH_DELAY * fs)
    ch = speaker_to_channel[SPEECH_SPEAKER]
    out[start:start + len(speech), ch] = speech
    log_event(__file__, SPEECH_SPEAKER, speech_file, round(speech_dur, 1))
    print(f"Speech speaker {SPEECH_SPEAKER} (ch {ch}): {speech_file} "
          f"at t={SPEECH_DELAY:.0f}s for {speech_dur:.1f}s")

    print(f"Playing {total:.0f}s total...")
    sd.play(out, samplerate=fs, device=DEVICE_ID)
    sd.wait()
    print("Done.")


if __name__ == "__main__":
    main()
