def stimulus(rng, cycles):
    rows = []
    def r(pv=0, ppc=0, tv=0, tt=0, tm=0, th=0, tpc=0, mid=None):
        d = {'areset':0,'predict_valid':pv,'predict_pc':ppc&0x7f,
             'train_valid':tv,'train_taken':tt,'train_mispredicted':tm,
             'train_history':th&0x7f,'train_pc':tpc&0x7f}
        if mid: d['mid']=mid
        rows.append(d)
    r(mid={'areset':1})
    r()
    r(mid={'areset':0})
    for i in range(4):
        r(pv=1, ppc=rng.getrandbits(7))
    for i in range(4):
        r(tv=1, tt=rng.getrandbits(1), tm=0, th=rng.getrandbits(7), tpc=rng.getrandbits(7))
    for i in range(3):
        r(pv=1, ppc=rng.getrandbits(7), tv=1, tt=rng.getrandbits(1), tm=1,
          th=rng.getrandbits(7), tpc=rng.getrandbits(7))
    r(pv=1, ppc=0, tv=1, tt=1, tm=1, th=0x7f, tpc=0x7f)
    r(pv=1, ppc=0x7f, tv=1, tt=0, tm=0, th=0, tpc=0)
    while len(rows) < cycles:
        pv = rng.getrandbits(1)
        tv = rng.getrandbits(1)
        tm = rng.getrandbits(1) if tv else 0
        mid = None
        if rng.random() < 0.15:
            mid = {'predict_valid': rng.getrandbits(1)}
        r(pv=pv, ppc=rng.getrandbits(7), tv=tv, tt=rng.getrandbits(1),
          tm=tm, th=rng.getrandbits(7), tpc=rng.getrandbits(7), mid=mid)
    return rows[:cycles]
