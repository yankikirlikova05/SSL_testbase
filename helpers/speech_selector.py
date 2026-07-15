# Pick a random file from speech/ and return it whole (no crop/loop).
# Returns (clip, filename). Helper only — imported by the play scripts.

import glob
import os
import random
from math import gcd

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

SPEECH_DIR = "speech"
fs = 48000
AMPLITUDE = 0.3 #changeable as well


def resample_to(x, sr):
    if sr == fs:
        return x
    g = gcd(sr, fs)
    return resample_poly(x, fs // g, sr // g)


def get_speech(amplitude=AMPLITUDE):
    files = sorted(glob.glob(os.path.join(SPEECH_DIR, "*.wav")) +
                   glob.glob(os.path.join(SPEECH_DIR, "*.mp3")))
    if not files:
        raise FileNotFoundError(f"No audio files in {SPEECH_DIR}/")
    path = random.choice(files)

    data, sr = sf.read(path, always_2d=False)
    if data.ndim > 1:                        # multi-channel -> mono
        data = data.mean(axis=1)
    data = data.astype(np.float64)
    data = resample_to(data, sr)             # whole file, no crop / loop

    peak = np.max(np.abs(data))              # peak-normalize to target level
    if peak > 0:
        data = data / peak * amplitude

    name = os.path.basename(path)
    print(f"Speech: {name} ({len(data) / fs:.1f}s)")
    return data, name
