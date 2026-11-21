def stimulus(rng, cycles):
    rows = []
    def rv(w): return rng.getrandbits(w)
    def add(**kw):
        d = {k: v for k, v in kw.items() if k != 'mid'}
        if 'mid' in kw: d['mid'] = kw['mid']
        rows.append(d)
    add(areset=1, predict_valid=0, predict_pc=0, train_valid=0, train_taken=0, train_mispredicted=0, train_history=0, train_pc=0)
    add(areset=1, predict_valid=1, predict_pc=5, train_valid=0, train_taken=0, train_mispredicted=0, train_history=0, train_pc=0)
    add(areset=0, predict_valid=1, predict_pc=10, train_valid=0, train_taken=0, train_mispredicted=0, train_history=0, train_pc=0)
    add(areset=0, predict_valid=1, predict_pc=20, train_valid=1, train_taken=1, train_mispredicted=0, train_history=3, train_pc=20)
    add(areset=0, predict_valid=1, predict_pc=30, train_valid=1, train_taken=0, train_mispredicted=1, train_history=7, train_pc=30)
    add(areset=0, predict_valid=0, predict_pc=0, train_valid=1, train_taken=1, train_mispredicted=1, train_history=15, train_pc=40)
    add(areset=0, predict_valid=1, predict_pc=50, train_valid=0, train_taken=0, train_mispredicted=0, train_history=0, train_pc=0)
    add(areset=0, predict_valid=1, predict_pc=60, train_valid=1, train_taken=1, train_mispredicted=0, train_history=31, train_pc=60)
    add(areset=0, predict_valid=1, predict_pc=70, train_valid=1, train_taken=0, train_mispredicted=1, train_history=63, train_pc=70)
    add(areset=0, predict_valid=1, predict_pc=80, train_valid=0, train_taken=0, train_mispredicted=0, train_history=0, train_pc=0)
    add(areset=0, predict_valid=0, predict_pc=0, train_valid=1, train_taken=1, train_mispredicted=0, train_history=127, train_pc=90)
    add(areset=0, predict_valid=1, predict_pc=100, train_valid=1, train_taken=0, train_mispredicted=0, train_history=1, train_pc=100)
    add(areset=0, predict_valid=1, predict_pc=110, train_valid=1, train_taken=1, train_mispredicted=1, train_history=2, train_pc=110)
    add(areset=0, predict_valid=1, predict_pc=120, train_valid=0, train_taken=0, train_mispredicted=0, train_history=0, train_pc=0)
    add(areset=0, predict_valid=0, predict_pc=0, train_valid=0, train_taken=0, train_mispredicted=0, train_history=0, train_pc=0)
    add(areset=0, predict_valid=1, predict_pc=127, train_valid=1, train_taken=1, train_mispredicted=0, train_history=127, train_pc=127)
    while len(rows) < cycles:
        pv = rng.getrandbits(1)
        tv = rng.getrandbits(1)
        tm = rng.getrandbits(1) if tv else 0
        tt = rng.getrandbits(1) if tv else 0
        row = dict(areset=0, predict_valid=pv, predict_pc=rv(7),
                   train_valid=tv, train_taken=tt, train_mispredicted=tm,
                   train_history=rv(7), train_pc=rv(7))
        if rng.random() < 0.3:
            row['mid'] = {'predict_valid': rng.getrandbits(1), 'train_valid': rng.getrandbits(1)}
        rows.append(row)
    return rows[:cycles]
