def db_to_amp(db):
    exponent = db / 20
    return 10 ** exponent
