def stimulus(rng, cycles):
    rows = []
    def rv():
        return rng.getrandbits(1)
    def rp():
        return rng.getrandbits(7)
    def rh():
        return rng.getrandbits(7)
    def row(areset=0, pv=0, ppc=0, tv=0, tt=0, tm=0, th=0, tpc=0, mid=None):
        d = {'areset': areset, 'predict_valid': pv, 'predict_pc': ppc,
             'train_valid': tv, 'train_taken': tt, 'train_mispredicted': tm,
             'train_history': th, 'train_pc': tpc}
        if mid is not None:
            d['mid'] = mid
        return d
    rows.append(row(areset=1))
    rows.append(row())
    rows.append(row(pv=1, ppc=0))
    rows.append(row(pv=1, ppc=1, tv=1, tt=1, tm=0, th=0, tpc=1))
    rows.append(row(pv=1, ppc=2, tv=1, tt=0, tm=1, th=3, tpc=2))
    rows.append(row(pv=1, ppc=3, tv=1, tt=1, tm=1, th=5, tpc=3))
    rows.append(row(pv=1, ppc=4, tv=1, tt=0, tm=0, th=7, tpc=4))
    rows.append(row(pv=1, ppc=5, tv=1, tt=1, tm=1, th=9, tpc=5))
    rows.append(row(pv=1, ppc=6, tv=1, tt=0, tm=1, th=11, tpc=6))
    rows.append(row(pv=1, ppc=7, tv=1, tt=1, tm=0, th=13, tpc=7))
    rows.append(row(pv=1, ppc=8, tv=1, tt=0, tm=0, th=15, tpc=8))
    rows.append(row(pv=1, ppc=9, tv=1, tt=1, tm=1, th=17, tpc=9))
    rows.append(row(pv=1, ppc=10, tv=1, tt=0, tm=1, th=19, tpc=10))
    rows.append(row(pv=1, ppc=11, tv=1, tt=1, tm=0, th=21, tpc=11))
    rows.append(row(pv=1, ppc=12, tv=1, tt=0, tm=0, th=23, tpc=12))
    rows.append(row(pv=1, ppc=13, tv=1, tt=1, tm=1, th=25, tpc=13))
    while len(rows) < cycles:
        a = 1 if rng.random() < 0.02 else 0
        pv = rv()
        tv = rv()
        rows.append(row(areset=a, pv=pv, ppc=rp(), tv=tv, tt=rv(), tm=rv(), th=rh(), tpc=rp()))
    return rows[:cycles]
