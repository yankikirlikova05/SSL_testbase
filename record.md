# Recording Run Order

Recommended order for running the playback scripts, from most basic to most
complex. Run every script **from the project root** (so the `speech/`, `urban/`
folders and `run_log.csv` resolve). Each speaker-playback event is auto-logged
to `run_log.csv`.

## 0. Calibration (do first, once)

| # | Script | What plays | Notes |
|---|--------|-----------|-------|
| 0 | `test_out.py` | Tone out of each channel in turn | Confirms which physical channel drives which speaker. Verify against `session_config.speaker_to_channel`. |
| — | `test/test_selectors.py` | Nothing (writes WAVs to `test/output/`) | Sanity-check that the selectors produce valid clips before a real session. |

## 1. Single sound source

| # | Script | What plays | Duration |
|---|--------|-----------|----------|
| 1 | `urban_noise.py` | One random 5 s urban clip from speakers 9–12 | ~5 s |
| 2 | `play_tone_1k.py` | Pure 1 kHz tone, speakers 7→8→1→2→3 | ~40 s |
| 3 | `play_tone_5k.py` | Pure 5 kHz tone, speakers 7→8→1→2→3 | ~40 s |
| 4 | `play_speech.py` | 4 random speech clips from random speakers (no noise) | ~22 s |

## 2. Two overlapping sources (signal + noise)

| # | Script | What plays | Duration |
|---|--------|-----------|----------|
| 5 | `play_tone_1k_noise.py` | 1 kHz tone sweep + continuous urban noise on 9–12 | ~40 s |
| 6 | `play_tone_5k_noise.py` | 5 kHz tone sweep + continuous urban noise on 9–12 | ~40 s |
| 7 | `play_urban_speech.py` | Urban noise on 9–12 + `speech1.wav` on speaker 1 | ~25 s |

## 3. Scenarios — noisy speech (most complex)

Each runs continuous urban noise on speakers 9–12 while speech plays on top.
Noiseless copies play the same speech with no background noise.

| # | Script | Sources | Layout | Duration |
|---|--------|---------|--------|----------|
| 8  | `play_scenario1.py` | 1 speaker + noise | 1 chunk swept across speakers 1→8, 3 s each, 2 s gap | ~44 s |
| 9  | `play_scenario2_noiseless.py` | 2 speakers, no noise | 9 pairs, 5 s each, 5 s gap | ~91 s |
| 10 | `play_scenario2.py` | 2 speakers + noise | same pairs, with background noise | ~91 s |
| 11 | `play_scenario3_noiseless.py` | 3 speakers, no noise | 7 groups, 5 s each, 5 s gap | ~71 s |
| 12 | `play_scenario3.py` | 3 speakers + noise | same groups, with background noise | ~71 s |




## File Names 

urban_trial01.wav
tone1k_trial01.wav
tone5k_trial01.wav
tone1k_noise_trial01.wav
tone5k_noise_trial01.wav
speech_trial01.wav
urbanspeech_trial01.wav
scn1_trial01.wav
scn2_noisy_trial01.wav
scn2_clean_trial01.wav
scn3_noisy_trial01.wav
scn3_clean_trial01.wav