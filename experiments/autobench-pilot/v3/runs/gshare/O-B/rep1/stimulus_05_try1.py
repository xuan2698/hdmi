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
    rows.append(rv(predict_valid=1, predict_pc=0x10, train_valid=1, train_taken=0, train_mispredicted=1, train_pc=0x10, train_history=0x7f))
    rows.append(rv(predict_valid=1, predict_pc=0x20, train_valid=1, train_taken=1, train_mispredicted=1, train_pc=0x20, train_history=0x55))
    rows.append(rv(predict_valid=1, predict_pc=0x30))
    rows.append(rv(predict_valid=1, predict_pc=0x30, train_valid=1, train_taken=1, train_pc=0x30, train_history=0x2a))
    rows.append(rv(predict_valid=1, predict_pc=0x40, train_valid=1, train_taken=0, train_mispredicted=1, train_pc=0x40, train_history=0x13))
    rows.append(rv(predict_valid=1, predict_pc=0x50))
    rows.append(rv(predict_valid=1, predict_pc=0x50, train_valid=1, train_taken=1, train_pc=0x50, train_history=0x3c))
    rows.append(rv(predict_valid=1, predict_pc=0x60, train_valid=1, train_taken=1, train_mispredicted=1, train_pc=0x60, train_history=0x0f))
    rows.append(rv(predict_valid=1, predict_pc=0x70))
    rows.append(rv(predict_valid=1, predict_pc=0x70, train_valid=1, train_taken=0, train_pc=0x70, train_history=0x66))
    rows.append(rv(predict_valid=1, predict_pc=0x01, train_valid=1, train_taken=1, train_mispredicted=1, train_pc=0x01, train_history=0x7e))
    while len(rows) < cycles:
        pv = rng.getrandbits(1)
        tv = rng.getrandbits(1)
        tm = rng.getrandbits(1) if tv else 0
        d = rv(
            predict_valid=pv,
            predict_pc=rng.getrandbits(7),
            train_valid=tv,
            train_taken=rng.getrandbits(1),
            train_mispredicted=tm,
            train_history=rng.getrandbits(7),
            train_pc=rng.getrandbits(7),
        )
        if rng.getrandbits(2) == 0:
            d['mid'] = {'predict_valid': rng.getrandbits(1), 'predict_pc': rng.getrandbits(7)}
        rows.append(d)
    return rows[:cycles]
