import csv
import os
from datetime import datetime

CSV_PATH = os.path.join(os.path.dirname(__file__), "run_log.csv")

HEADER = ["date", "time", "script", "source_count",
          "speakers", "angles", "sounds", "duration_s", "notes"]

# Speaker -> true angle in degrees. 1-8 form the ring around the array at 45°
# intervals. 9-12 are noise speakers facing outward, so they have no DOA angle
# (logged blank).
SPEAKER_ANGLES = {
    1: 0,
    2: 45,
    3: 90,
    4: 135,
    5: 180,
    6: 225,
    7: 270,
    8: 315,
    9: None,
    10: None,
    11: None,
    12: None,
}


def _ensure_header():
    if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0:
        with open(CSV_PATH, "w", newline="") as f:
            csv.writer(f).writerow(HEADER)


def log_event(script, speakers, sounds, duration_s, notes=""):
    _ensure_header()

    if isinstance(speakers, int):
        speakers = [speakers]
    if isinstance(sounds, str):
        sounds = [sounds] * len(speakers)

    angles = [SPEAKER_ANGLES.get(s) for s in speakers]
    now = datetime.now()

    row = [
        now.strftime("%Y-%m-%d"),
        now.strftime("%H:%M"),
        os.path.basename(script),
        len(speakers),
        ",".join(str(s) for s in speakers),
        ",".join("" if a is None else str(a) for a in angles),
        "; ".join(sounds),
        duration_s,
        notes,
    ]
    with open(CSV_PATH, "a", newline="") as f:
        csv.writer(f).writerow(row)


def show(n=20):
    if not os.path.exists(CSV_PATH):
        print("No log yet.")
        return
    with open(CSV_PATH, newline="") as f:
        rows = list(csv.reader(f))
    for row in rows[:1] + rows[1:][-n:]:
        print("\t".join(row))


if __name__ == "__main__":
    show()
