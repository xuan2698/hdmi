def stimulus(rng, cycles):
    rows = []
    def rv():
        return {
            'areset': 0, 'predict_valid': 0, 'predict_pc': 0,
            'train_valid': 0, 'train_taken': 0, 'train_mispredicted': 0,
            'train_history': 0, 'train_pc': 0
        }
    r = rv(); r['areset'] = 1; rows.append(r)
    r = rv(); rows.append(r)
    for i in range(cycles - 2):
        r = rv()
        if i < 4:
            r['predict_valid'] = 1
            r['predict_pc'] = rng.getrandbits(7)
            if i == 2:
                r['train_valid'] = 1
                r['train_taken'] = rng.getrandbits(1)
                r['train_mispredicted'] = rng.getrandbits(1)
                r['train_history'] = rng.getrandbits(7)
                r['train_pc'] = rng.getrandbits(7)
        elif i < 8:
            r['train_valid'] = 1
            r['train_taken'] = rng.getrandbits(1)
            r['train_mispredicted'] = rng.getrandbits(1)
            r['train_history'] = rng.getrandbits(7)
            r['train_pc'] = rng.getrandbits(7)
            if i % 2 == 0:
                r['predict_valid'] = 1
                r['predict_pc'] = rng.getrandbits(7)
        else:
            r['predict_valid'] = rng.getrandbits(1)
            r['predict_pc'] = rng.getrandbits(7)
            r['train_valid'] = rng.getrandbits(1)
            r['train_taken'] = rng.getrandbits(1)
            r['train_mispredicted'] = rng.getrandbits(1)
            r['train_history'] = rng.getrandbits(7)
            r['train_pc'] = rng.getrandbits(7)
        rows.append(r)
    return rows[:cycles]
