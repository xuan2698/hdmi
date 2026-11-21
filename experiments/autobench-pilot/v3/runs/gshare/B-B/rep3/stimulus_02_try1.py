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
    rows.append(row(areset=1, pv=1, ppc=rp()))
    rows.append(row(areset=0))
    rows.append(row(pv=1, ppc=rp()))
    rows.append(row(pv=1, ppc=rp(), tv=1, tt=rv(), tm=rv(), th=rh(), tpc=rp()))
    rows.append(row(pv=1, ppc=rp(), tv=1, tt=1, tm=1, th=rh(), tpc=rp()))
    rows.append(row(pv=1, ppc=rp(), tv=1, tt=0, tm=0, th=rh(), tpc=rp()))
    rows.append(row(pv=1, ppc=rp(), tv=1, tt=1, tm=0, th=rh(), tpc=rp(),
                    mid={'predict_valid': 0}))
    rows.append(row(pv=0, tv=1, tt=rv(), tm=rv(), th=rh(), tpc=rp()))
    rows.append(row(pv=1, ppc=rp(), tv=1, tt=rv(), tm=1, th=rh(), tpc=rp(),
                    mid={'train_valid': 0, 'predict_valid': 1, 'predict_pc': rp()}))
    rows.append(row(areset=1, pv=1, ppc=rp(), tv=1, tt=1, tm=1, th=rh(), tpc=rp()))
    rows.append(row(areset=0, pv=1, ppc=rp()))
    while len(rows) < cycles:
        pv = rv()
        tv = rv()
        tm = rv() if tv else 0
        tt = rv() if tv else 0
        mid = None
        if rng.random() < 0.3:
            mid = {}
            if rv():
                mid['predict_valid'] = rv()
                mid['predict_pc'] = rp()
            if rv():
                mid['train_valid'] = rv()
                mid['train_taken'] = rv()
                mid['train_mispredicted'] = rv()
                mid['train_history'] = rh()
                mid['train_pc'] = rp()
        rows.append(row(areset=0, pv=pv, ppc=rp(), tv=tv, tt=tt, tm=tm,
                        th=rh(), tpc=rp(), mid=mid))
    return rows[:cycles]
