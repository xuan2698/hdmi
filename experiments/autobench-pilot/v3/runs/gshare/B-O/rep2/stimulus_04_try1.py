def stimulus(rng, cycles):
    rows = []
    def r(pv=0, ppc=0, tv=0, tt=0, tm=0, th=0, tpc=0, mid=None):
        d = {'areset':0,'predict_valid':pv,'predict_pc':ppc,'train_valid':tv,
             'train_taken':tt,'train_mispredicted':tm,'train_history':th,'train_pc':tpc}
        if mid: d['mid'] = mid
        rows.append(d)
    r(1)
    r(1)
    r(0, 0, 0, 0, 0, 0, 0)
    for i in range(4):
        r(1, rng.randrange(128), 0, 0, 0, 0, 0)
    for i in range(4):
        r(0, 0, 1, rng.getrandbits(1), 0, rng.randrange(128), rng.randrange(128))
    for i in range(3):
        r(1, rng.randrange(128), 1, rng.getrandbits(1), rng.getrandbits(1),
          rng.randrange(128), rng.randrange(128))
    r(1, 5, 1, 1, 1, 10, 5, mid={'predict_valid':0})
    r(1, 5, 1, 0, 0, 10, 5, mid={'train_valid':0})
    r(1, 0, 1, 1, 1, 0, 0, mid={'predict_pc':64})
    while len(rows) < cycles:
        pv = rng.getrandbits(1)
        tv = rng.getrandbits(1)
        mid = None
        if rng.random() < 0.3:
            mid = {'predict_valid': rng.getrandbits(1), 'train_valid': rng.getrandbits(1)}
        r(pv, rng.randrange(128), tv, rng.getrandbits(1), rng.getrandbits(1),
          rng.randrange(128), rng.randrange(128), mid)
    return rows[:cycles]
