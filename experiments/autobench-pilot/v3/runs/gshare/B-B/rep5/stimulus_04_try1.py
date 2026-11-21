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
        r(1, rng.randrange(128), 1, rng.getrandbits(1), 0, rng.randrange(128), rng.randrange(128))
    for i in range(3):
        r(1, rng.randrange(128), 1, rng.getrandbits(1), 1, rng.randrange(128), rng.randrange(128))
    r(0, 0, 1, 1, 1, 0, 0, {'predict_valid':1,'predict_pc':5})
    r(1, 5, 0, 0, 0, 0, 0, {'train_valid':1,'train_taken':0,'train_mispredicted':1,'train_history':3,'train_pc':7})
    r(1, 10, 1, 1, 0, 20, 30, {'predict_valid':0})
    r(0, 0, 0, 0, 0, 0, 0)
    while len(rows) < cycles:
        pv = rng.getrandbits(1)
        tv = rng.getrandbits(1)
        d = {'areset':0,
             'predict_valid':pv,'predict_pc':rng.randrange(128),
             'train_valid':tv,'train_taken':rng.getrandbits(1),
             'train_mispredicted':rng.getrandbits(1) if tv else 0,
             'train_history':rng.randrange(128),'train_pc':rng.randrange(128)}
        if rng.random() < 0.3:
            d['mid'] = {'predict_valid':rng.getrandbits(1),'predict_pc':rng.randrange(128)}
        rows.append(d)
    return rows[:cycles]
