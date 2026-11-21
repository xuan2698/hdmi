def stimulus(rng, cycles):
    rows = []
    def rv(): return rng.getrandbits(1)
    def rp(): return rng.getrandbits(7)
    def rh(): return rng.getrandbits(7)
    def row(**kw):
        d = {'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':0,
             'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0}
        d.update(kw)
        return d
    rows.append(row(areset=1))
    rows.append(row(areset=1, predict_valid=1, predict_pc=rp()))
    rows.append(row(areset=0))
    rows.append(row(predict_valid=1, predict_pc=0))
    rows.append(row(predict_valid=1, predict_pc=0, train_valid=1, train_taken=1, train_pc=0, train_history=0))
    rows.append(row(predict_valid=1, predict_pc=0, train_valid=1, train_taken=0, train_mispredicted=1, train_pc=0, train_history=0))
    rows.append(row(train_valid=1, train_taken=1, train_mispredicted=1, train_pc=rp(), train_history=rh()))
    rows.append(row(predict_valid=1, predict_pc=rp(), train_valid=1, train_taken=1, train_mispredicted=1, train_pc=rp(), train_history=rh()))
    rows.append(row(predict_valid=1, predict_pc=rp()))
    rows.append(row(train_valid=1, train_taken=0, train_pc=rp(), train_history=rh()))
    rows.append(row(predict_valid=1, predict_pc=rp(), train_valid=1, train_taken=1, train_pc=rp(), train_history=rh()))
    rows.append(row(areset=1, predict_valid=1, predict_pc=rp(), train_valid=1, train_taken=1, train_mispredicted=1, train_pc=rp(), train_history=rh()))
    rows.append(row(areset=0))
    rows.append(row(predict_valid=1, predict_pc=rp(), train_valid=1, train_taken=0, train_mispredicted=1, train_pc=rp(), train_history=rh()))
    rows.append(row(predict_valid=1, predict_pc=rp()))
    rows.append(row(train_valid=1, train_taken=1, train_mispredicted=1, train_pc=rp(), train_history=rh()))
    while len(rows) < cycles:
        r = row()
        r['predict_valid'] = rv()
        r['predict_pc'] = rp()
        r['train_valid'] = rv()
        r['train_taken'] = rv()
        r['train_mispredicted'] = rv()
        r['train_history'] = rh()
        r['train_pc'] = rp()
        if rng.random() < 0.1:
            r['areset'] = 1
        if rng.random() < 0.3:
            r['mid'] = {'predict_valid': rv(), 'train_valid': rv(), 'train_taken': rv(),
                        'train_mispredicted': rv(), 'train_history': rh(), 'train_pc': rp(),
                        'predict_pc': rp()}
        rows.append(r)
    return rows[:cycles]
