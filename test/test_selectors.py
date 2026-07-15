import os
import sys

import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)   # so the selector modules can be imported
os.chdir(ROOT)             # so the selectors find the speech/ and urban/ folders

from speech_selector import get_speech
from urban_noise_selector import get_urban_noise

fs = 48000
OUT_DIR = os.path.join(ROOT, "test", "output")
N_EACH = 3 
DURATION = 5.0


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    for i in range(N_EACH):
        clip, name = get_speech(duration=DURATION)
        path = os.path.join(OUT_DIR, f"speech_{i + 1}.wav")
        sf.write(path, clip, fs)
        print(f"wrote {path}  (from {name})")

    for i in range(N_EACH):
        clip, name = get_urban_noise(duration=DURATION)
        path = os.path.join(OUT_DIR, f"urban_{i + 1}.wav")
        sf.write(path, clip, fs)
        print(f"wrote {path}  (from {name})")

    print("done")


if __name__ == "__main__":
    main()
