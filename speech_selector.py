# Pick a random file from speech/, crop a random fixed-duration segment, return it.
# Helper only — imported by the play scripts, does not play anything itself.

import glob
import os
import random
from math import gcd

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

SPEECH_DIR = "speech"
CLIP_DURATION = 10.0  #TODO:change as needed
fs = 48000
AMPLITUDE = 0.3 #changeable as well


def resample_to(x, sr):
    if sr == fs:
        return x
    g = gcd(sr, fs)
    return resample_poly(x, fs // g, sr // g)


def get_speech(duration=CLIP_DURATION, amplitude=AMPLITUDE):
    files = sorted(glob.glob(os.path.join(SPEECH_DIR, "*.wav")) +
                   glob.glob(os.path.join(SPEECH_DIR, "*.mp3")))
    if not files:
        raise FileNotFoundError(f"No audio files in {SPEECH_DIR}/")
    path = random.choice(files)

    data, sr = sf.read(path, always_2d=False)
    if data.ndim > 1:                        # multi-channel -> mono
        data = data.mean(axis=1)
    data = data.astype(np.float64)
    data = resample_to(data, sr)

    n = int(duration * fs)
    if len(data) < n:                        # too short -> tile to cover duration
        data = np.tile(data, int(np.ceil(n / len(data))))
    start = random.randint(0, len(data) - n)  # random crop position
    clip = data[start:start + n]

    peak = np.max(np.abs(clip))              # peak-normalize to target level
    if peak > 0:
        clip = clip / peak * amplitude

    print(f"Speech: {os.path.basename(path)} "
          f"crop {duration:.0f}s at t={start / fs:.1f}s")
    return clip
