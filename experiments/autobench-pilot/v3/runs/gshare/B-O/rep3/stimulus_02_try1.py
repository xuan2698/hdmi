def stimulus(rng, cycles):
    rows = []
    def r(pv=0, ppc=0, tv=0, tt=0, tm=0, th=0, tpc=0, ar=0, mid=None):
        d = {'areset': ar, 'predict_valid': pv, 'predict_pc': ppc & 0x7f,
             'train_valid': tv, 'train_taken': tt, 'train_mispredicted': tm,
             'train_history': th & 0x7f, 'train_pc': tpc & 0x7f}
        if mid is not None:
            d['mid'] = mid
        rows.append(d)
    r(ar=1)
    r(ar=1)
    r()
    r(pv=1, ppc=0)
    r(pv=1, ppc=0x7f)
    r(pv=1, ppc=0x55, tv=1, tt=1, tm=0, th=0, tpc=0x55)
    r(pv=1, ppc=0x2a, tv=1, tt=0, tm=1, th=0x7f, tpc=0x2a)
    r(pv=1, ppc=0x13, tv=1, tt=1, tm=1, th=0x55, tpc=0x13)
    r(pv=1, ppc=0x40, tv=1, tt=0, tm=0, th=0x2a, tpc=0x40)
    r(pv=1, ppc=0x01, tv=1, tt=1, tm=0, th=0x01, tpc=0x01)
    r(pv=1, ppc=0x7e, tv=1, tt=0, tm=1, th=0x3c, tpc=0x7e)
    r(pv=1, ppc=0x33, tv=1, tt=1, tm=1, th=0x66, tpc=0x33)
    r(pv=1, ppc=0x0f, tv=1, tt=0, tm=0, th=0x0f, tpc=0x0f)
    r(pv=1, ppc=0x70, tv=1, tt=1, tm=0, th=0x70, tpc=0x70)
    r(pv=1, ppc=0x21, tv=1, tt=0, tm=1, th=0x21, tpc=0x21)
    r(pv=1, ppc=0x5a, tv=1, tt=1, tm=1, th=0x5a, tpc=0x5a)
    while len(rows) < cycles:
        pv = rng.getrandbits(1)
        tv = rng.getrandbits(1)
        ar = 1 if rng.random() < 0.02 else 0
        ppc = rng.getrandbits(7)
        tpc = rng.getrandbits(7)
        tt = rng.getrandbits(1)
        tm = rng.getrandbits(1)
        th = rng.getrandbits(7)
        mid = None
        if rng.random() < 0.15:
            mid = {'predict_valid': rng.getrandbits(1),
                   'train_valid': rng.getrandbits(1),
                   'train_taken': rng.getrandbits(1),
                   'train_mispredicted': rng.getrandbits(1),
                   'train_history': rng.getrandbits(7),
                   'train_pc': rng.getrandbits(7),
                   'predict_pc': rng.getrandbits(7)}
        r(pv=pv, ppc=ppc, tv=tv, tt=tt, tm=tm, th=th, tpc=tpc, ar=ar, mid=mid)
    return rows[:cycles]
