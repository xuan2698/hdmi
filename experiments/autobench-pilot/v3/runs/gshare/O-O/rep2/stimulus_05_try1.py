def stimulus(rng, cycles):
    rows = []
    def row(**kw):
        d = {'areset': 0, 'predict_valid': 0, 'predict_pc': 0,
             'train_valid': 0, 'train_taken': 0, 'train_mispredicted': 0,
             'train_history': 0, 'train_pc': 0}
        d.update(kw)
        rows.append(d)
    row(areset=1)
    row(areset=1, predict_valid=1, predict_pc=0x10)
    row(areset=0)
    row(predict_valid=1, predict_pc=0x05)
    row(predict_valid=1, predict_pc=0x05, train_valid=1, train_taken=1,
        train_history=0x05, train_pc=0x05)
    row(predict_valid=1, predict_pc=0x05, train_valid=1, train_taken=0,
        train_mispredicted=1, train_history=0x2A, train_pc=0x05)
    row(predict_valid=1, predict_pc=0x7F, train_valid=1, train_taken=1,
        train_history=0x55, train_pc=0x7F)
    row(predict_valid=1, predict_pc=0x00, train_valid=1, train_taken=1,
        train_mispredicted=1, train_history=0x7F, train_pc=0x00)
    row(predict_valid=1, predict_pc=0x3C, train_valid=1, train_taken=0,
        train_history=0x3C, train_pc=0x3C)
    row(predict_valid=1, predict_pc=0x3C, train_valid=1, train_taken=1,
        train_mispredicted=1, train_history=0x00, train_pc=0x3C)
    row(predict_valid=1, predict_pc=0x11, train_valid=1, train_taken=1,
        train_history=0x11, train_pc=0x11)
    row(predict_valid=1, predict_pc=0x22, train_valid=1, train_taken=0,
        train_mispredicted=1, train_history=0x22, train_pc=0x22)
    row(predict_valid=1, predict_pc=0x33, train_valid=1, train_taken=1,
        train_history=0x33, train_pc=0x33)
    row(predict_valid=1, predict_pc=0x44, train_valid=1, train_taken=0,
        train_history=0x44, train_pc=0x44)
    row(predict_valid=1, predict_pc=0x55, train_valid=1, train_taken=1,
        train_mispredicted=1, train_history=0x55, train_pc=0x55)
    row(predict_valid=1, predict_pc=0x66, train_valid=1, train_taken=0,
        train_history=0x66, train_pc=0x66)
    while len(rows) < cycles:
        pv = rng.getrandbits(1)
        tv = rng.getrandbits(1)
        d = {
            'areset': 0,
            'predict_valid': pv,
            'predict_pc': rng.getrandbits(7) if pv else 0,
            'train_valid': tv,
            'train_taken': rng.getrandbits(1) if tv else 0,
            'train_mispredicted': rng.getrandbits(1) if tv else 0,
            'train_history': rng.getrandbits(7) if tv else 0,
            'train_pc': rng.getrandbits(7) if tv else 0,
        }
        if rng.random() < 0.3:
            d['mid'] = {'predict_valid': rng.getrandbits(1),
                        'train_valid': rng.getrandbits(1)}
        rows.append(d)
    return rows[:cycles]
