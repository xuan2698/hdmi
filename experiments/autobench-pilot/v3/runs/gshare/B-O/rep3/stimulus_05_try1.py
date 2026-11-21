def stimulus(rng, cycles):
    rows = []
    def rv():
        return {
            'areset': 0, 'predict_valid': 0, 'predict_pc': 0,
            'train_valid': 0, 'train_taken': 0, 'train_mispredicted': 0,
            'train_history': 0, 'train_pc': 0
        }
    rows.append({'areset': 1, 'predict_valid': 0, 'predict_pc': 0,
                 'train_valid': 0, 'train_taken': 0, 'train_mispredicted': 0,
                 'train_history': 0, 'train_pc': 0})
    rows.append({'areset': 0, 'predict_valid': 0, 'predict_pc': 0,
                 'train_valid': 0, 'train_taken': 0, 'train_mispredicted': 0,
                 'train_history': 0, 'train_pc': 0})
    for i in range(4):
        r = rv()
        r['predict_valid'] = 1
        r['predict_pc'] = rng.randrange(128)
        rows.append(r)
    for i in range(4):
        r = rv()
        r['train_valid'] = 1
        r['train_taken'] = rng.getrandbits(1)
        r['train_mispredicted'] = rng.getrandbits(1)
        r['train_history'] = rng.randrange(128)
        r['train_pc'] = rng.randrange(128)
        rows.append(r)
    for i in range(3):
        r = rv()
        r['predict_valid'] = 1
        r['predict_pc'] = rng.randrange(128)
        r['train_valid'] = 1
        r['train_taken'] = rng.getrandbits(1)
        r['train_mispredicted'] = rng.getrandbits(1)
        r['train_history'] = rng.randrange(128)
        r['train_pc'] = rng.randrange(128)
        rows.append(r)
    while len(rows) < cycles:
        r = rv()
        r['predict_valid'] = rng.getrandbits(1)
        r['predict_pc'] = rng.randrange(128)
        r['train_valid'] = rng.getrandbits(1)
        r['train_taken'] = rng.getrandbits(1)
        r['train_mispredicted'] = rng.getrandbits(1)
        r['train_history'] = rng.randrange(128)
        r['train_pc'] = rng.randrange(128)
        if rng.random() < 0.3:
            r['mid'] = {'predict_valid': rng.getrandbits(1),
                        'train_valid': rng.getrandbits(1)}
        rows.append(r)
    return rows[:cycles]
