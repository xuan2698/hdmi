def stimulus(rng, cycles):
    rows = []
    def rv(w): return rng.getrandbits(w)
    def rp(): return rv(7)
    def rh(): return rv(7)
    def row(**kw):
        d = {'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0}
        d.update(kw)
        return d
    rows.append(row(areset=1))
    rows.append(row(areset=1, predict_valid=1, predict_pc=rp(), train_valid=1, train_taken=1, train_mispredicted=1, train_history=rh(), train_pc=rp()))
    rows.append(row())
    rows.append(row(predict_valid=1, predict_pc=rp()))
    rows.append(row(predict_valid=1, predict_pc=rp(), train_valid=1, train_taken=1, train_mispredicted=0, train_history=rh(), train_pc=rp()))
    rows.append(row(predict_valid=1, predict_pc=rp(), train_valid=1, train_taken=0, train_mispredicted=1, train_history=rh(), train_pc=rp()))
    rows.append(row(train_valid=1, train_taken=1, train_mispredicted=1, train_history=rh(), train_pc=rp()))
    rows.append(row(predict_valid=1, predict_pc=rp(), train_valid=1, train_taken=1, train_mispredicted=1, train_history=rh(), train_pc=rp()))
    rows.append(row(predict_valid=1, predict_pc=rp(), train_valid=1, train_taken=0, train_mispredicted=0, train_history=rh(), train_pc=rp()))
    rows.append(row(predict_valid=1, predict_pc=rp()))
    rows.append(row(train_valid=1, train_taken=1, train_mispredicted=0, train_history=rh(), train_pc=rp()))
    rows.append(row(predict_valid=1, predict_pc=rp(), train_valid=1, train_taken=1, train_mispredicted=0, train_history=rh(), train_pc=rp()))
    rows.append(row(predict_valid=1, predict_pc=rp(), train_valid=1, train_taken=0, train_mispredicted=1, train_history=rh(), train_pc=rp()))
    rows.append(row(areset=1, predict_valid=1, predict_pc=rp(), train_valid=1, train_taken=1, train_mispredicted=1, train_history=rh(), train_pc=rp()))
    rows.append(row())
    rows.append(row(predict_valid=1, predict_pc=rp(), train_valid=1, train_taken=1, train_mispredicted=1, train_history=rh(), train_pc=rp()))
    while len(rows) < cycles:
        pv = rng.getrandbits(1)
        tv = rng.getrandbits(1)
        d = row(
            areset=1 if rng.random() < 0.02 else 0,
            predict_valid=pv,
            predict_pc=rp() if pv else 0,
            train_valid=tv,
            train_taken=rng.getrandbits(1) if tv else 0,
            train_mispredicted=rng.getrandbits(1) if tv else 0,
            train_history=rh() if tv else 0,
            train_pc=rp() if tv else 0,
        )
        if rng.random() < 0.3:
            d['mid'] = {'predict_valid': rng.getrandbits(1), 'train_valid': rng.getrandbits(1)}
        rows.append(d)
    return rows[:cycles]
