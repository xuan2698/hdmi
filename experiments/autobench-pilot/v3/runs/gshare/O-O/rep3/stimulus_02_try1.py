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
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 1, 'train_valid': 1,
                 'train_taken': 0, 'train_mispredicted': 1, 'train_history': 1, 'train_pc': 1})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 2, 'train_valid': 1,
                 'train_taken': 1, 'train_mispredicted': 1, 'train_history': 2, 'train_pc': 2})
    rows.append({'areset': 0, 'predict_valid': 0, 'predict_pc': 0, 'train_valid': 1,
                 'train_taken': 0, 'train_mispredicted': 1, 'train_history': 3, 'train_pc': 3})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 4, 'train_valid': 0,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 5, 'train_valid': 1,
                 'train_taken': 1, 'train_mispredicted': 0, 'train_history': 4, 'train_pc': 5})
    rows.append({'areset': 0, 'predict_valid': 0, 'predict_pc': 0, 'train_valid': 1,
                 'train_taken': 1, 'train_mispredicted': 1, 'train_history': 5, 'train_pc': 6})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 7, 'train_valid': 1,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 6, 'train_pc': 7})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 8, 'train_valid': 0,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0})
    rows.append({'areset': 0, 'predict_valid': 0, 'predict_pc': 0, 'train_valid': 1,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 7, 'train_pc': 8})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 9, 'train_valid': 1,
                 'train_taken': 1, 'train_mispredicted': 1, 'train_history': 8, 'train_pc': 9})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 10, 'train_valid': 0,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0})
    rows.append({'areset': 0, 'predict_valid': 0, 'predict_pc': 0, 'train_valid': 1,
                 'train_taken': 1, 'train_mispredicted': 0, 'train_history': 9, 'train_pc': 10})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_pc': 11, 'train_valid': 1,
                 'train_taken': 0, 'train_mispredicted': 1, 'train_history': 10, 'train_pc': 11})
    while len(rows) < cycles:
        r = rv()
        if rng.random() < 0.3:
            r['mid'] = {'predict_valid': rng.getrandbits(1), 'train_valid': rng.getrandbits(1)}
        rows.append(r)
    return rows[:cycles]
