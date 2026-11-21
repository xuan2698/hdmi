def stimulus(rng, cycles):
    rows = []
    def r(pv=0, ppc=0, tv=0, tt=0, tm=0, th=0, tpc=0, ar=0, mid=None):
        d = {'areset': ar, 'predict_valid': pv, 'predict_pc': ppc & 127,
             'train_valid': tv, 'train_taken': tt, 'train_mispredicted': tm,
             'train_history': th & 127, 'train_pc': tpc & 127}
        if mid is not None:
            d['mid'] = mid
        rows.append(d)
    r(ar=1)
    r(ar=1, pv=1, ppc=5)
    r()
    r(pv=1, ppc=0)
    r(pv=1, ppc=1)
    r(pv=1, ppc=2)
    r(pv=1, ppc=3)
    r(tv=1, tt=1, th=0, tpc=0)
    r(tv=1, tt=0, th=1, tpc=1)
    r(tv=1, tt=1, tm=1, th=2, tpc=2)
    r(pv=1, ppc=4, tv=1, tt=0, tm=1, th=3, tpc=3)
    r(pv=1, ppc=5, tv=1, tt=1, tm=0, th=4, tpc=4)
    r(pv=1, ppc=6, tv=1, tt=0, tm=1, th=5, tpc=5, mid={'predict_valid': 0})
    r(pv=1, ppc=7, tv=1, tt=1, tm=0, th=6, tpc=6, mid={'train_valid': 0})
    r(pv=1, ppc=8, tv=1, tt=0, tm=1, th=7, tpc=7, mid={'areset': 1})
    r(ar=1, pv=1, ppc=9, tv=1, tt=1, tm=1, th=8, tpc=8)
    while len(rows) < cycles:
        pv = rng.getrandbits(1)
        tv = rng.getrandbits(1)
        ar = 1 if rng.random() < 0.03 else 0
        mid = None
        if rng.random() < 0.15:
            mid = {}
            if rng.random() < 0.5:
                mid['predict_valid'] = rng.getrandbits(1)
            if rng.random() < 0.5:
                mid['train_valid'] = rng.getrandbits(1)
            if rng.random() < 0.2:
                mid['areset'] = rng.getrandbits(1)
        r(pv=pv, ppc=rng.randrange(128), tv=tv, tt=rng.getrandbits(1),
          tm=rng.getrandbits(1), th=rng.randrange(128), tpc=rng.randrange(128),
          ar=ar, mid=mid)
    return rows[:cycles]
