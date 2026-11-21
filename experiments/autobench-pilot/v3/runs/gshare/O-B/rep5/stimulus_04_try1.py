def stimulus(rng, cycles):
    rows = []
    def row(**kw):
        d = {}
        for k, v in kw.items():
            d[k] = v
        rows.append(d)
    row(areset=1, predict_valid=0, predict_pc=0, train_valid=0, train_taken=0, train_mispredicted=0, train_history=0, train_pc=0)
    row(areset=1, predict_valid=0, predict_pc=0, train_valid=0, train_taken=0, train_mispredicted=0, train_history=0, train_pc=0)
    row(areset=0, predict_valid=0, predict_pc=0, train_valid=0, train_taken=0, train_mispredicted=0, train_history=0, train_pc=0)
    for i in range(cycles - 3):
        pv = rng.getrandbits(1)
        tv = rng.getrandbits(1)
        ppc = rng.getrandbits(7)
        tpc = rng.getrandbits(7)
        tt = rng.getrandbits(1)
        tm = rng.getrandbits(1)
        th = rng.getrandbits(7)
        d = dict(areset=0, predict_valid=pv, predict_pc=ppc, train_valid=tv,
                 train_taken=tt, train_mispredicted=tm, train_history=th, train_pc=tpc)
        if i % 5 == 0:
            d['mid'] = dict(predict_valid=rng.getrandbits(1), train_valid=rng.getrandbits(1))
        rows.append(d)
    return rows[:cycles]
