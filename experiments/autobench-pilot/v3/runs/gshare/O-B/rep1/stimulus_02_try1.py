def stimulus(rng, cycles):
    rows = []
    def rv():
        return rng.getrandbits(1)
    def rp():
        return rng.getrandbits(7)
    def rh():
        return rng.getrandbits(7)
    def row(**kw):
        d = {'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':0,
             'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0}
        d.update(kw)
        return d
    rows.append(row(areset=1))
    rows.append(row(areset=1, predict_valid=1, predict_pc=rp()))
    rows.append(row())
    rows.append(row(predict_valid=1, predict_pc=0))
    rows.append(row(predict_valid=1, predict_pc=1))
    rows.append(row(predict_valid=1, predict_pc=127))
    rows.append(row(train_valid=1, train_taken=1, train_pc=0, train_history=0))
    rows.append(row(train_valid=1, train_taken=0, train_pc=1, train_history=1))
    rows.append(row(train_valid=1, train_taken=1, train_mispredicted=1, train_pc=2, train_history=2))
    rows.append(row(train_valid=1, train_taken=0, train_mispredicted=1, train_pc=3, train_history=3))
    rows.append(row(predict_valid=1, predict_pc=4, train_valid=1, train_taken=1, train_pc=4, train_history=4))
    rows.append(row(predict_valid=1, predict_pc=5, train_valid=1, train_taken=0, train_mispredicted=1, train_pc=5, train_history=5))
    rows.append(row(predict_valid=1, predict_pc=6, train_valid=1, train_taken=1, train_mispredicted=1, train_pc=6, train_history=6))
    rows.append(row(areset=1, predict_valid=1, predict_pc=7, train_valid=1, train_taken=1, train_pc=7, train_history=7))
    rows.append(row(areset=1, train_valid=1, train_taken=0, train_mispredicted=1, train_pc=8, train_history=8))
    rows.append(row(predict_valid=1, predict_pc=9, train_valid=1, train_taken=1, train_mispredicted=1, train_pc=9, train_history=9))
    while len(rows) < cycles:
        pv = rv()
        tv = rv()
        d = row(
            areset=1 if rng.random() < 0.03 else 0,
            predict_valid=pv,
            predict_pc=rp() if pv else 0,
            train_valid=tv,
            train_taken=rv() if tv else 0,
            train_mispredicted=rv() if tv else 0,
            train_history=rh() if tv else 0,
            train_pc=rp() if tv else 0,
        )
        if rng.random() < 0.15:
            mid = {}
            if rng.random() < 0.5:
                mid['predict_valid'] = rv()
                if mid['predict_valid']:
                    mid['predict_pc'] = rp()
            if rng.random() < 0.5:
                mid['train_valid'] = rv()
                if mid['train_valid']:
                    mid['train_taken'] = rv()
                    mid['train_mispredicted'] = rv()
                    mid['train_history'] = rh()
                    mid['train_pc'] = rp()
            if rng.random() < 0.1:
                mid['areset'] = 1
            d['mid'] = mid
        rows.append(d)
    return rows[:cycles]
