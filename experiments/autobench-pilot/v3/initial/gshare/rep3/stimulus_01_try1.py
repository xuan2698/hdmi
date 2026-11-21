def stimulus(rng, cycles):
    rows = []
    hist = 0
    pcs = [rng.randrange(128) for _ in range(8)]
    def add(pv, ppc, tv, tt, tm, th, tpc, mid=None):
        r = {'areset': 0, 'predict_valid': pv, 'predict_pc': ppc & 127,
             'train_valid': tv, 'train_taken': tt, 'train_mispredicted': tm,
             'train_history': th & 127, 'train_pc': tpc & 127}
        if mid: r['mid'] = mid
        rows.append(r)
    rows.append({'areset': 1, 'predict_valid': 0, 'predict_pc': 0, 'train_valid': 0,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0})
    rows.append({'areset': 0, 'predict_valid': 0, 'predict_pc': 0, 'train_valid': 0,
                 'train_taken': 0, 'train_mispredicted': 0, 'train_history': 0, 'train_pc': 0})
    for i in range(cycles - 2):
        pv = rng.getrandbits(1)
        tv = rng.getrandbits(1)
        ppc = rng.choice(pcs)
        tpc = rng.choice(pcs)
        tt = rng.getrandbits(1)
        tm = rng.getrandbits(1) if tv else 0
        th = rng.randrange(128)
        mid = None
        if rng.random() < 0.3:
            mid = {'predict_valid': rng.getrandbits(1), 'train_valid': rng.getrandbits(1)}
        add(pv, ppc, tv, tt, tm, th, tpc, mid)
    return rows[:cycles]
