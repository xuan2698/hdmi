def stimulus(rng, cycles):
    rows = []
    rows.append({'areset': 1, 'predict_valid': 0, 'predict_taken': 0, 'train_mispredicted': 0, 'train_taken': 0, 'train_history': 0})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_taken': 1, 'train_mispredicted': 0, 'train_taken': 0, 'train_history': 0})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_taken': 0, 'train_mispredicted': 0, 'train_taken': 0, 'train_history': 0})
    rows.append({'areset': 0, 'predict_valid': 0, 'predict_taken': 0, 'train_mispredicted': 1, 'train_taken': 1, 'train_history': 0xAAAAAAAA})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_taken': 1, 'train_mispredicted': 1, 'train_taken': 0, 'train_history': 0x55555555})
    rows.append({'areset': 0, 'predict_valid': 0, 'predict_taken': 0, 'train_mispredicted': 0, 'train_taken': 0, 'train_history': 0})
    rows.append({'areset': 1, 'predict_valid': 1, 'predict_taken': 1, 'train_mispredicted': 1, 'train_taken': 1, 'train_history': 0xFFFFFFFF})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_taken': 0, 'train_mispredicted': 0, 'train_taken': 0, 'train_history': 0})
    while len(rows) < cycles:
        r = rng.randrange(8)
        if r == 0:
            rows.append({'areset': 1, 'predict_valid': rng.getrandbits(1), 'predict_taken': rng.getrandbits(1), 'train_mispredicted': rng.getrandbits(1), 'train_taken': rng.getrandbits(1), 'train_history': rng.getrandbits(32)})
        elif r == 1:
            rows.append({'areset': 0, 'predict_valid': 1, 'predict_taken': rng.getrandbits(1), 'train_mispredicted': 0, 'train_taken': 0, 'train_history': rng.getrandbits(32)})
        elif r == 2:
            rows.append({'areset': 0, 'predict_valid': 0, 'predict_taken': 0, 'train_mispredicted': 1, 'train_taken': rng.getrandbits(1), 'train_history': rng.getrandbits(32)})
        elif r == 3:
            rows.append({'areset': 0, 'predict_valid': 1, 'predict_taken': rng.getrandbits(1), 'train_mispredicted': 1, 'train_taken': rng.getrandbits(1), 'train_history': rng.getrandbits(32)})
        else:
            rows.append({'areset': 0, 'predict_valid': rng.getrandbits(1), 'predict_taken': rng.getrandbits(1), 'train_mispredicted': rng.getrandbits(1), 'train_taken': rng.getrandbits(1), 'train_history': rng.getrandbits(32)})
    return rows[:cycles]
