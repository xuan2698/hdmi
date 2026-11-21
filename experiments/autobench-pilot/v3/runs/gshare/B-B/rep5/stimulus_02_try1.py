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
    r(ar=0)
    for i in range(6):
        r(pv=1, ppc=rng.randrange(128))
    r(pv=1, ppc=0x05, tv=1, tt=1, tm=0, th=0x11, tpc=0x05)
    r(pv=1, ppc=0x05, tv=1, tt=0, tm=1, th=0x22, tpc=0x05)
    r(pv=1, ppc=0x05, tv=1, tt=1, tm=0, th=0x33, tpc=0x05,
      mid={'predict_valid': 0})
    r(pv=0, tv=1, tt=0, tm=1, th=0x44, tpc=0x05)
    r(pv=1, ppc=0x05, tv=1, tt=1, tm=0, th=0x55, tpc=0x05)
    r(ar=1, pv=1, ppc=0x7f, tv=1, tt=1, tm=1, th=0x7f, tpc=0x7f)
    r(ar=0)
    while len(rows) < cycles:
        pv = rng.getrandbits(1)
        tv = rng.getrandbits(1)
        tm = rng.getrandbits(1) if tv else 0
        tt = rng.getrandbits(1) if tv else 0
        mid = None
        if rng.random() < 0.2:
            mid = {'predict_valid': rng.getrandbits(1),
                   'train_valid': rng.getrandbits(1)}
        r(pv=pv, ppc=rng.randrange(128), tv=tv, tt=tt, tm=tm,
          th=rng.randrange(128), tpc=rng.randrange(128),
          ar=1 if rng.random() < 0.03 else 0, mid=mid)
    return rows[:cycles]
