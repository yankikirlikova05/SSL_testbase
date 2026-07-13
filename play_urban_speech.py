# Play urban noise from speakers 9,10,11,12 and speech1.wav from speaker 1

import glob
import os
from math import gcd

import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.signal import resample_poly

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

AMPLITUDE = 0.3
URBAN_DIR = "urban"
SPEECH_FILE = "speech1.wav"
NOISE_SPEAKERS = [9, 10, 11, 12]
SPEECH_SPEAKER = 1

SPEECH_DELAY = 5.0   
SPEECH_DURATION = 15.0
NOISE_TAIL = 5.0 
TOTAL_DURATION = SPEECH_DELAY + SPEECH_DURATION + NOISE_TAIL


def resample_to(x, sr):
    if sr == fs:
        return x
    g = gcd(sr, fs)
    return resample_poly(x, fs // g, sr // g)


def fit_length(x, n):
    if len(x) < n:
        x = np.tile(x, int(np.ceil(n / len(x))))
    return x[:n]


def load_source(path, n_samples):
    data, sr = sf.read(path, always_2d=False)
    if data.ndim > 1: 
        data = data.mean(axis=1)
    data = data.astype(np.float64)
    data = resample_to(data, sr)
    peak = np.max(np.abs(data))
    if peak > 0:
        data = data / peak * AMPLITUDE
    data = fit_length(data, n_samples)
    return data


def main():
    total_n = int(TOTAL_DURATION * fs)
    out = np.zeros((total_n, N_CHANNELS_OUT))

    urban_files = sorted(glob.glob(os.path.join(URBAN_DIR, "*.mp3")))
    for spk, f in zip(NOISE_SPEAKERS, urban_files):
        ch = speaker_to_channel[spk]
        out[:, ch] = load_source(f, total_n)
        print(f"Noise  speaker {spk} (ch {ch}): {os.path.basename(f)}")

    speech = load_source(SPEECH_FILE, int(SPEECH_DURATION * fs))
    start = int(SPEECH_DELAY * fs)
    ch = speaker_to_channel[SPEECH_SPEAKER]
    out[start:start + len(speech), ch] = speech
    print(f"Speech speaker {SPEECH_SPEAKER} (ch {ch}): {SPEECH_FILE} "
          f"at t={SPEECH_DELAY:.0f}s for {SPEECH_DURATION:.0f}s")

    print(f"Playing {TOTAL_DURATION:.0f}s total...")
    sd.play(out, samplerate=fs, device=DEVICE_ID)
    sd.wait()
    print("Done.")


if __name__ == "__main__":
    main()
