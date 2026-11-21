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
    r(ar=1, pv=1, ppc=0x12)
    r(ar=0, pv=1, ppc=0x34)
    r(ar=0, pv=1, ppc=0x56, tv=1, tt=1, tm=0, th=0x11, tpc=0x56)
    r(ar=0, pv=1, ppc=0x78, tv=1, tt=0, tm=1, th=0x22, tpc=0x78)
    r(ar=0, pv=1, ppc=0x1a, tv=1, tt=1, tm=1, th=0x33, tpc=0x1a)
    r(ar=0, pv=1, ppc=0x2b, tv=1, tt=0, tm=0, th=0x44, tpc=0x2b)
    r(ar=0, pv=1, ppc=0x3c, tv=1, tt=1, tm=0, th=0x55, tpc=0x3c)
    r(ar=0, pv=1, ppc=0x4d, tv=1, tt=0, tm=1, th=0x66, tpc=0x4d)
    r(ar=0, pv=1, ppc=0x5e, tv=1, tt=1, tm=1, th=0x77, tpc=0x5e)
    r(ar=0, pv=1, ppc=0x6f, tv=1, tt=0, tm=0, th=0x00, tpc=0x6f)
    r(ar=0, pv=1, ppc=0x70, tv=1, tt=1, tm=0, th=0x7f, tpc=0x70)
    r(ar=0, pv=1, ppc=0x01, tv=1, tt=0, tm=1, th=0x3f, tpc=0x01)
    r(ar=0, pv=1, ppc=0x02, tv=1, tt=1, tm=1, th=0x40, tpc=0x02)
    r(ar=0, pv=1, ppc=0x03, tv=1, tt=0, tm=0, th=0x01, tpc=0x03)
    r(ar=0, pv=1, ppc=0x04, tv=1, tt=1, tm=0, th=0x02, tpc=0x04)
    while len(rows) < cycles:
        pv = rng.getrandbits(1)
        tv = rng.getrandbits(1)
        ar = 1 if rng.randrange(100) < 2 else 0
        mid = None
        if rng.randrange(100) < 20:
            mid = {'predict_valid': rng.getrandbits(1),
                   'train_valid': rng.getrandbits(1),
                   'train_taken': rng.getrandbits(1),
                   'train_mispredicted': rng.getrandbits(1)}
        r(ar=ar, pv=pv, ppc=rng.getrandbits(7),
          tv=tv, tt=rng.getrandbits(1), tm=rng.getrandbits(1),
          th=rng.getrandbits(7), tpc=rng.getrandbits(7), mid=mid)
    return rows[:cycles]
