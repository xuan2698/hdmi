def stimulus(rng, cycles):
    rows = []
    def rv():
        return {
            'areset': 0,
            'predict_valid': rng.getrandbits(1),
            'predict_pc': rng.getrandbits(7),
            'train_valid': rng.getrandbits(1),
            'train_taken': rng.getrandbits(1),
            'train_mispredicted': rng.getrandbits(1),
            'train_history': rng.getrandbits(7),
            'train_pc': rng.getrandbits(7),
        }
    rows.append({'areset': 1, 'predict_valid': 0, 'predict_pc': 0, 'train_valid': 0,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 0, 'train_valid': 0,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0})
    rows.append({'areset': 0, 'predict_valid': 0, 'predict_pc': 0, 'train_valid': 1,
                 'train_taken': 1, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 5, 'train_valid': 1,
                 'train_taken': 0, 'train_mispredicted': 1, 'train_history': 0x55, 'train_pc': 5})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 0x7f, 'train_valid': 1,
                 'train_taken': 1, 'train_mispredicted': 1, 'train_history': 0x7f, 'train_pc': 0x7f})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 0x2a, 'train_valid': 0,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0})
    rows.append({'areset': 0, 'predict_valid': 0, 'predict_pc': 0, 'train_valid': 1,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0x2a, 'train_pc': 0x2a})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 0x2a, 'train_valid': 0,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 0x2a, 'train_valid': 0,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 0x2a, 'train_valid': 0,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0})
    rows.append({'areset': 0, 'predict_valid': 0, 'predict_pc': 0, 'train_valid': 1,
                 'train_taken': 1, 'train_mispredicted': 0, 'train_history': 0x2a, 'train_pc': 0x2a})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 0x2a, 'train_valid': 0,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 0x2a, 'train_valid': 0,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 0x2a, 'train_valid': 0,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 0x2a, 'train_valid': 0,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 0x2a, 'train_valid': 0,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0})
    while len(rows) < cycles:
        r = rv()
        if rng.random() < 0.3:
            r['mid'] = {'predict_valid': rng.getrandbits(1), 'train_valid': rng.getrandbits(1)}
        rows.append(r)
    return rows[:cycles]
