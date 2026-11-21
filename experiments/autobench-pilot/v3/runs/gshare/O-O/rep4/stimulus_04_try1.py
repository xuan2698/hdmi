def stimulus(rng, cycles):
    rows = []
    def rv(w): return rng.getrandbits(w)
    def row(**kw):
        d = {k: v for k, v in kw.items() if k != 'mid'}
        if 'mid' in kw: d['mid'] = kw['mid']
        rows.append(d)
    row(areset=1, predict_valid=0, predict_pc=0, train_valid=0, train_taken=0, train_mispredicted=0, train_history=0, train_pc=0)
    row(areset=1, predict_valid=1, predict_pc=rv(7), train_valid=1, train_taken=1, train_mispredicted=0, train_history=rv(7), train_pc=rv(7))
    row(areset=0, predict_valid=0, predict_pc=0, train_valid=0, train_taken=0, train_mispredicted=0, train_history=0, train_pc=0)
    for i in range(4):
        row(areset=0, predict_valid=1, predict_pc=rv(7), train_valid=0, train_taken=0, train_mispredicted=0, train_history=0, train_pc=0)
    for i in range(4):
        row(areset=0, predict_valid=0, predict_pc=0, train_valid=1, train_taken=rng.getrandbits(1), train_mispredicted=0, train_history=rv(7), train_pc=rv(7))
    for i in range(3):
        row(areset=0, predict_valid=1, predict_pc=rv(7), train_valid=1, train_taken=rng.getrandbits(1), train_mispredicted=1, train_history=rv(7), train_pc=rv(7))
    while len(rows) < cycles:
        pv = rng.getrandbits(1)
        tv = rng.getrandbits(1)
        tm = rng.getrandbits(1) if tv else 0
        d = dict(areset=0,
                 predict_valid=pv, predict_pc=rv(7) if pv else 0,
                 train_valid=tv, train_taken=rng.getrandbits(1) if tv else 0,
                 train_mispredicted=tm,
                 train_history=rv(7) if tv else 0,
                 train_pc=rv(7) if tv else 0)
        if rng.getrandbits(2) == 0:
            d['mid'] = {'predict_valid': rng.getrandbits(1), 'train_valid': rng.getrandbits(1)}
        rows.append(d)
    return rows[:cycles]
