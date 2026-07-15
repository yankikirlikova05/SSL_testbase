# Shared helper for the multi-trial runner scripts.
# Runs a play script N_TRIALS times as a fresh subprocess (from the project
# root, so speech/, urban/ and run_log.csv resolve), waiting WAIT_BETWEEN
# seconds between trials.

import os
import subprocess
import sys
import time

from trial_config import N_TRIALS, WAIT_BETWEEN, STOP_ON_ERROR

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_trials(play_script):
    for trial in range(1, N_TRIALS + 1):
        print(f"[{play_script}] trial {trial}/{N_TRIALS}")
        result = subprocess.run([sys.executable, play_script], cwd=ROOT)

        if result.returncode != 0:
            msg = f"[{play_script}] trial {trial} exited with code {result.returncode}"
            if STOP_ON_ERROR:
                raise SystemExit(msg)
            print(msg + " - continuing")

        if trial < N_TRIALS:
            print(f"waiting {WAIT_BETWEEN:.0f}s before next trial...")
            time.sleep(WAIT_BETWEEN)

    print(f"[{play_script}] done - {N_TRIALS} trials")
