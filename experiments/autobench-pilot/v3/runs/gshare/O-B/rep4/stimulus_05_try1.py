def stimulus(rng, cycles):
    rows = []
    def r(pv=0, ppc=0, tv=0, tt=0, tm=0, th=0, tpc=0, mid=None):
        d = {'areset': 0, 'predict_valid': pv, 'predict_pc': ppc & 0x7f,
             'train_valid': tv, 'train_taken': tt, 'train_mispredicted': tm,
             'train_history': th & 0x7f, 'train_pc': tpc & 0x7f}
        if mid is not None:
            d['mid'] = mid
        rows.append(d)
    r(0, 0, 0, 0, 0, 0, 0, {'areset': 1})
    r()
    r()
    r(pv=1, ppc=0x00)
    r(pv=1, ppc=0x01)
    r(pv=1, ppc=0x02)
    r(pv=1, ppc=0x03)
    r(tv=1, tt=1, tm=0, th=0x00, tpc=0x00)
    r(tv=1, tt=0, tm=1, th=0x01, tpc=0x01)
    r(pv=1, ppc=0x04, tv=1, tt=1, tm=0, th=0x02, tpc=0x02)
    r(pv=1, ppc=0x05, tv=1, tt=0, tm=1, th=0x03, tpc=0x03)
    r(pv=1, ppc=0x06, tv=1, tt=1, tm=1, th=0x04, tpc=0x04)
    r(pv=1, ppc=0x07, tv=1, tt=0, tm=0, th=0x05, tpc=0x05)
    r(pv=1, ppc=0x08, tv=1, tt=1, tm=0, th=0x06, tpc=0x06)
    r(pv=1, ppc=0x09, tv=1, tt=0, tm=1, th=0x07, tpc=0x07)
    r(pv=1, ppc=0x0a, tv=1, tt=1, tm=1, th=0x08, tpc=0x08)
    while len(rows) < cycles:
        pv = rng.getrandbits(1)
        tv = rng.getrandbits(1)
        ppc = rng.randrange(128)
        tpc = rng.randrange(128)
        tt = rng.getrandbits(1)
        tm = rng.getrandbits(1)
        th = rng.randrange(128)
        mid = None
        if rng.random() < 0.3:
            mid = {'predict_valid': rng.getrandbits(1),
                   'train_valid': rng.getrandbits(1),
                   'train_mispredicted': rng.getrandbits(1)}
        r(pv, ppc, tv, tt, tm, th, tpc, mid)
    return rows[:cycles]
