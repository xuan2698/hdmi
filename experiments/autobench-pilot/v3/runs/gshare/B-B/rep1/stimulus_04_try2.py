def stimulus(rng, cycles):
    rows = []
    def r(areset=0, pv=0, ppc=0, tv=0, tt=0, tm=0, th=0, tpc=0, mid=None):
        d = {'areset': areset, 'predict_valid': pv, 'predict_pc': ppc & 0x7f,
             'train_valid': tv, 'train_taken': tt, 'train_mispredicted': tm,
             'train_history': th & 0x7f, 'train_pc': tpc & 0x7f}
        if mid: d['mid'] = mid
        rows.append(d)
    r(areset=1)
    r(areset=1)
    r()
    for i in range(6):
        r(pv=1, ppc=rng.getrandbits(7))
    for i in range(6):
        r(tv=1, tt=rng.getrandbits(1), tm=0, th=rng.getrandbits(7), tpc=rng.getrandbits(7))
    for i in range(4):
        r(tv=1, tt=rng.getrandbits(1), tm=1, th=rng.getrandbits(7), tpc=rng.getrandbits(7))
    for i in range(3):
        r(pv=1, ppc=rng.getrandbits(7), tv=1, tt=rng.getrandbits(1), tm=0,
          th=rng.getrandbits(7), tpc=rng.getrandbits(7))
    for i in range(3):
        r(pv=1, ppc=rng.getrandbits(7), tv=1, tt=rng.getrandbits(1), tm=1,
          th=rng.getrandbits(7), tpc=rng.getrandbits(7))
    while len(rows) < cycles:
        k = rng.randrange(4)
        if k == 0:
            r(pv=1, ppc=rng.getrandbits(7))
        elif k == 1:
            r(tv=1, tt=rng.getrandbits(1), tm=rng.getrandbits(1),
              th=rng.getrandbits(7), tpc=rng.getrandbits(7))
        elif k == 2:
            r(pv=1, ppc=rng.getrandbits(7), tv=1, tt=rng.getrandbits(1),
              tm=rng.getrandbits(1), th=rng.getrandbits(7), tpc=rng.getrandbits(7))
        else:
            r()
    return rows[:cycles]
