DEVICE_ID = 4 
N_CHANNELS_OUT = 16 
fs = 48000 

SOURCE_GAIN = -14   # dB (converted to linear amplitude via utils.db_to_amp)
NOISE_GAIN = -10    # dB
NOISE_SPEAKERS = [9, 10, 11, 12] 

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
