def stimulus(rng, cycles):
    rows = []
    def rv(**kw):
        d = {'areset': 0, 'predict_valid': 0, 'predict_pc': 0, 'train_valid': 0,
             'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0}
        d.update(kw)
        return d
    rows.append(rv(areset=1))
    rows.append(rv(areset=1, predict_valid=1, predict_pc=5))
    rows.append(rv(areset=0))
    rows.append(rv(predict_valid=1, predict_pc=0x10))
    rows.append(rv(predict_valid=1, predict_pc=0x10, train_valid=1, train_taken=1, train_pc=0x10, train_history=0))
    rows.append(rv(predict_valid=1, predict_pc=0x10, train_valid=1, train_taken=0, train_mispredicted=1, train_pc=0x10, train_history=0x40))
    rows.append(rv(predict_valid=1, predict_pc=0x20, train_valid=1, train_taken=1, train_mispredicted=1, train_pc=0x20, train_history=0x7f))
    rows.append(rv(predict_valid=1, predict_pc=0x30, train_valid=1, train_taken=1, train_pc=0x30, train_history=0x55))
    rows.append(rv(predict_valid=1, predict_pc=0x30, train_valid=1, train_taken=0, train_mispredicted=1, train_pc=0x30, train_history=0x2a))
    rows.append(rv(predict_valid=1, predict_pc=0x30, train_valid=1, train_taken=1, train_pc=0x30, train_history=0x2a))
    rows.append(rv(predict_valid=1, predict_pc=0x30, train_valid=1, train_taken=1, train_pc=0x30, train_history=0x2a))
    rows.append(rv(predict_valid=1, predict_pc=0x30, train_valid=1, train_taken=1, train_pc=0x30, train_history=0x2a))
    rows.append(rv(predict_valid=1, predict_pc=0x30, train_valid=1, train_taken=1, train_pc=0x30, train_history=0x2a))
    rows.append(rv(predict_valid=1, predict_pc=0x30, train_valid=1, train_taken=1, train_pc=0x30, train_history=0x2a))
    rows.append(rv(predict_valid=1, predict_pc=0x30, train_valid=1, train_taken=1, train_pc=0x30, train_history=0x2a))
    rows.append(rv(predict_valid=1, predict_pc=0x30, train_valid=1, train_taken=1, train_pc=0x30, train_history=0x2a))
    while len(rows) < cycles:
        r = rv()
        if rng.random() < 0.85:
            r['predict_valid'] = 1
            r['predict_pc'] = rng.getrandbits(7)
        if rng.random() < 0.6:
            r['train_valid'] = 1
            r['train_taken'] = rng.getrandbits(1)
            r['train_mispredicted'] = 1 if rng.random() < 0.3 else 0
            r['train_history'] = rng.getrandbits(7)
            r['train_pc'] = rng.getrandbits(7)
        if rng.random() < 0.1:
            r['areset'] = 1
        if rng.random() < 0.15:
            r['mid'] = {'predict_pc': rng.getrandbits(7)}
        rows.append(r)
    return rows[:cycles]
