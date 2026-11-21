def stimulus(rng, cycles):
    rows = []
    def rv(**kw):
        d = {'areset': 0, 'predict_valid': 0, 'predict_pc': 0, 'train_valid': 0,
             'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0}
        d.update(kw)
        return d
    rows.append(rv(areset=1))
    rows.append(rv(areset=1))
    rows.append(rv())
    for i in range(cycles - 3):
        d = rv()
        d['predict_valid'] = rng.getrandbits(1)
        d['predict_pc'] = rng.randrange(128)
        d['train_valid'] = rng.getrandbits(1)
        d['train_taken'] = rng.getrandbits(1)
        d['train_mispredicted'] = rng.getrandbits(1)
        d['train_history'] = rng.randrange(128)
        d['train_pc'] = rng.randrange(128)
        if rng.random() < 0.3:
            d['mid'] = {'predict_valid': rng.getrandbits(1),
                        'train_valid': rng.getrandbits(1),
                        'train_mispredicted': rng.getrandbits(1)}
        rows.append(d)
    return rows[:cycles]
