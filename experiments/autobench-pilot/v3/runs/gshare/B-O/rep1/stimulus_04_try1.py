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
        elif i < 8:
            r['train_valid'] = 1
            r['train_taken'] = rng.getrandbits(1)
            r['train_mispredicted'] = rng.getrandbits(1)
            r['train_history'] = rng.getrandbits(7)
            r['train_pc'] = rng.getrandbits(7)
        elif i < 12:
            r['predict_valid'] = 1
            r['predict_pc'] = rng.getrandbits(7)
            r['train_valid'] = 1
            r['train_taken'] = rng.getrandbits(1)
            r['train_mispredicted'] = rng.getrandbits(1)
            r['train_history'] = rng.getrandbits(7)
            r['train_pc'] = rng.getrandbits(7)
        else:
            r['predict_valid'] = rng.getrandbits(1)
            r['predict_pc'] = rng.getrandbits(7)
            r['train_valid'] = rng.getrandbits(1)
            r['train_taken'] = rng.getrandbits(1)
            r['train_mispredicted'] = rng.getrandbits(1)
            r['train_history'] = rng.getrandbits(7)
            r['train_pc'] = rng.getrandbits(7)
        if rng.random() < 0.3:
            m = {}
            if rng.random() < 0.5:
                m['predict_valid'] = rng.getrandbits(1)
                m['predict_pc'] = rng.getrandbits(7)
            if rng.random() < 0.5:
                m['train_valid'] = rng.getrandbits(1)
                m['train_taken'] = rng.getrandbits(1)
                m['train_mispredicted'] = rng.getrandbits(1)
                m['train_history'] = rng.getrandbits(7)
                m['train_pc'] = rng.getrandbits(7)
            r['mid'] = m
        rows.append(r)
    return rows
