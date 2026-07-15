# Generate a filename for a Raspberry Pi mic-array recording.
# One recording per play-script run. The trial number auto-increments per
# condition (scans the recordings folder). Timestamp is intentionally left off:
# the Pi's CSV log already maps each filename to its capture time.
#
#   name pattern:  <condition>_trial<NN>.wav
#   example:       scn2_noisy_trial03.wav
#
# Usage on the Pi (inside record_1min.py, before you start capturing):
#   from recording_name import recording_name
#   fname = recording_name("play_scenario2")   # -> next free trial for scn2_noisy

import glob
import os

REC_DIR = "lab_recordings"

# play script name -> short condition code used in the filename
CONDITION_CODES = {
    "urban_noise": "urban",
    "play_tone_1k": "tone1k",
    "play_tone_5k": "tone5k",
    "play_tone_1k_noise": "tone1k_noise",
    "play_tone_5k_noise": "tone5k_noise",
    "play_speech": "speech",
    "play_urban_speech": "urbanspeech",
    "play_scenario1": "scn1",
    "play_scenario2": "scn2_noisy",
    "play_scenario2_noiseless": "scn2_clean",
    "play_scenario3": "scn3_noisy",
    "play_scenario3_noiseless": "scn3_clean",
}


def _code(condition):
    """Accept a script name, a path, or a bare code and return the code."""
    base = os.path.splitext(os.path.basename(condition))[0]
    return CONDITION_CODES.get(base, base)


def next_trial(code, rec_dir=REC_DIR):
    """Return the next unused trial number for a condition in rec_dir."""
    trials = []
    for f in glob.glob(os.path.join(rec_dir, f"{code}_trial*")):
        tag = os.path.basename(f).split("_trial")[-1][:2]
        if tag.isdigit():
            trials.append(int(tag))
    return max(trials, default=0) + 1


def recording_name(condition, trial=None, rec_dir=REC_DIR):
    """Build a recording filename for a condition.

    condition : play-script name (e.g. "play_scenario2") or a bare code
    trial     : trial number; if None, the next free one is auto-detected
    """
    code = _code(condition)
    if trial is None:
        trial = next_trial(code, rec_dir)
    return f"{code}_trial{trial:02d}.wav"


if __name__ == "__main__":
    import sys
    cond = sys.argv[1] if len(sys.argv) > 1 else "play_scenario2"
    print(recording_name(cond))
