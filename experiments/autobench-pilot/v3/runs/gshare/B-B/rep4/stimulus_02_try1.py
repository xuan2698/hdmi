def stimulus(rng, cycles):
    rows = []
    def r(pv=0, ppc=0, tv=0, tt=0, tm=0, th=0, tpc=0, ar=0, mid=None):
        d = {'areset': ar, 'predict_valid': pv, 'predict_pc': ppc & 0x7f,
             'train_valid': tv, 'train_taken': tt & 1, 'train_mispredicted': tm & 1,
             'train_history': th & 0x7f, 'train_pc': tpc & 0x7f}
        if mid is not None:
            d['mid'] = mid
        rows.append(d)
    r(ar=1)
    r(ar=1, pv=1, ppc=0x12)
    r(ar=0)
    r(pv=1, ppc=0x00)
    r(pv=1, ppc=0x7f, tv=1, tt=1, tm=0, th=0x00, tpc=0x7f)
    r(pv=1, ppc=0x01, tv=1, tt=0, tm=1, th=0x55, tpc=0x01)
    r(pv=1, ppc=0x02, tv=1, tt=1, tm=1, th=0x2a, tpc=0x02)
    r(pv=1, ppc=0x03, tv=1, tt=0, tm=0, th=0x7f, tpc=0x03)
    r(pv=1, ppc=0x04, tv=1, tt=1, tm=0, th=0x01, tpc=0x04)
    r(pv=1, ppc=0x05, tv=1, tt=0, tm=1, th=0x3c, tpc=0x05)
    r(pv=1, ppc=0x06, tv=1, tt=1, tm=1, th=0x6e, tpc=0x06)
    r(pv=1, ppc=0x07, tv=1, tt=0, tm=0, th=0x11, tpc=0x07)
    r(pv=1, ppc=0x08, tv=1, tt=1, tm=0, th=0x22, tpc=0x08)
    r(pv=1, ppc=0x09, tv=1, tt=0, tm=1, th=0x33, tpc=0x09)
    r(pv=1, ppc=0x0a, tv=1, tt=1, tm=1, th=0x44, tpc=0x0a)
    r(pv=1, ppc=0x0b, tv=1, tt=0, tm=0, th=0x55, tpc=0x0b)
    while len(rows) < cycles:
        pv = rng.getrandbits(1)
        tv = rng.getrandbits(1)
        ar = 1 if rng.random() < 0.02 else 0
        ppc = rng.randrange(128)
        tpc = rng.randrange(128)
        tt = rng.getrandbits(1)
        tm = rng.getrandbits(1)
        th = rng.randrange(128)
        mid = None
        if rng.random() < 0.15:
            mid = {'predict_valid': rng.getrandbits(1),
                   'train_valid': rng.getrandbits(1),
                   'train_taken': rng.getrandbits(1),
                   'train_mispredicted': rng.getrandbits(1),
                   'train_history': rng.randrange(128),
                   'train_pc': rng.randrange(128),
                   'predict_pc': rng.randrange(128)}
        r(pv=pv, ppc=ppc, tv=tv, tt=tt, tm=tm, th=th, tpc=tpc, ar=ar, mid=mid)
    return rows[:cycles]
