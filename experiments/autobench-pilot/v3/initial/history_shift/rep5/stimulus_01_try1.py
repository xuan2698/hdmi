def stimulus(rng, cycles):
    rows = []
    rows.append({'areset': 1, 'predict_valid': 0, 'predict_taken': 0, 'train_mispredicted': 0, 'train_taken': 0, 'train_history': 0})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_taken': 1, 'train_mispredicted': 0, 'train_taken': 0, 'train_history': 0})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_taken': 0, 'train_mispredicted': 0, 'train_taken': 0, 'train_history': 0})
    rows.append({'areset': 0, 'predict_valid': 0, 'predict_taken': 0, 'train_mispredicted': 1, 'train_taken': 1, 'train_history': 0xAAAAAAAA})
    rows.append({'areset': 0, 'predict_valid': 1, 'predict_taken': 1, 'train_mispredicted': 1, 'train_taken': 0, 'train_history': 0x55555555})
    rows.append({'areset': 0, 'predict_valid': 0, 'predict_taken': 0, 'train_mispredicted': 0, 'train_taken': 0, 'train_history': 0})
    rows.append({'areset': 1, 'predict_valid': 1, 'predict_taken': 1, 'train_mispredicted': 1, 'train_taken': 1, 'train_history': 0xFFFFFFFF})
    rows.append({'areset': 0, 'predict_valid': 0, 'predict_taken': 0, 'train_mispredicted': 0, 'train_taken': 0, 'train_history': 0})
    while len(rows) < cycles:
        r = {}
        r['areset'] = 1 if rng.random() < 0.02 else 0
        r['predict_valid'] = rng.getrandbits(1)
        r['predict_taken'] = rng.getrandbits(1)
        r['train_mispredicted'] = 1 if rng.random() < 0.15 else 0
        r['train_taken'] = rng.getrandbits(1)
        r['train_history'] = rng.getrandbits(32)
        if rng.random() < 0.2:
            m = {}
            if rng.random() < 0.5:
                m['predict_valid'] = rng.getrandbits(1)
                m['predict_taken'] = rng.getrandbits(1)
            if rng.random() < 0.5:
                m['train_mispredicted'] = rng.getrandbits(1)
                m['train_taken'] = rng.getrandbits(1)
                m['train_history'] = rng.getrandbits(32)
            r['mid'] = m
        rows.append(r)
    return rows[:cycles]
