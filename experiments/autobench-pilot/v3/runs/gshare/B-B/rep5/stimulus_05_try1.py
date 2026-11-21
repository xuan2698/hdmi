def stimulus(rng, cycles):
    rows = []
    def r(pv=0, ppc=0, tv=0, tt=0, tm=0, th=0, tpc=0, mid=None):
        d = {'areset':0,'predict_valid':pv,'predict_pc':ppc&0x7f,
             'train_valid':tv,'train_taken':tt,'train_mispredicted':tm,
             'train_history':th&0x7f,'train_pc':tpc&0x7f}
        if mid: d['mid']=mid
        rows.append(d)
    r(0,0,0,0,0,0,0,{'areset':1})
    r(0,0,0,0,0,0,0,{'areset':0})
    for i in range(4):
        r(1, rng.randrange(128), 0,0,0,0,0)
    for i in range(4):
        r(0,0,1, rng.getrandbits(1), rng.getrandbits(1), rng.randrange(128), rng.randrange(128))
    for i in range(4):
        r(1, rng.randrange(128), 1, rng.getrandbits(1), rng.getrandbits(1), rng.randrange(128), rng.randrange(128))
    while len(rows) < cycles:
        pv = rng.getrandbits(1)
        tv = rng.getrandbits(1)
        r(pv, rng.randrange(128), tv, rng.getrandbits(1), rng.getrandbits(1),
          rng.randrange(128), rng.randrange(128))
    return rows[:cycles]
