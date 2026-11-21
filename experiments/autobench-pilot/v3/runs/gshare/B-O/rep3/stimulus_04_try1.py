def stimulus(rng, cycles):
    rows = []
    def r():
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
    rows.append({'areset': 0, 'predict_valid': 0, 'predict_pc': 0, 'train_valid': 0,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0})
    for i in range(4):
        d = r()
        d['predict_valid'] = 1
        d['train_valid'] = 0
        rows.append(d)
    for i in range(4):
        d = r()
        d['train_valid'] = 1
        d['predict_valid'] = 0
        rows.append(d)
    for i in range(4):
        d = r()
        d['predict_valid'] = 1
        d['train_valid'] = 1
        d['train_mispredicted'] = 1
        rows.append(d)
    while len(rows) < cycles:
        d = r()
        if rng.random() < 0.3:
            d['predict_valid'] = 1
            d['train_valid'] = 1
        rows.append(d)
    return rows[:cycles]
