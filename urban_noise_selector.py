# Pick a random file from urban/, crop a random fixed-duration segment, return/save it.

import glob
import os
import random
from math import gcd

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

URBAN_DIR = "urban"
CROP_DURATION = 10.0 # TODO: change as needed
fs = 48000
AMPLITUDE = 0.3


def resample_to(x, sr):
    if sr == fs:
        return x
    g = gcd(sr, fs)
    return resample_poly(x, fs // g, sr // g)


def get_urban_noise(duration=CROP_DURATION, amplitude=AMPLITUDE):
    files = sorted(glob.glob(os.path.join(URBAN_DIR, "*.wav")) +
                   glob.glob(os.path.join(URBAN_DIR, "*.mp3")))
    if not files:
        raise FileNotFoundError(f"No audio files in {URBAN_DIR}/")
    path = random.choice(files)

    data, sr = sf.read(path, always_2d=False)
    if data.ndim > 1: 
        data = data.mean(axis=1)
    data = data.astype(np.float64)
    data = resample_to(data, sr)

    n = int(duration * fs)
    if len(data) < n: 
        data = np.tile(data, int(np.ceil(n / len(data))))
    start = random.randint(0, len(data) - n)
    clip = data[start:start + n]

    peak = np.max(np.abs(clip))
    if peak > 0:
        clip = clip / peak * amplitude

    print(f"Urban noise: {os.path.basename(path)} "
          f"crop {duration:.0f}s at t={start / fs:.1f}s")
    return clip
