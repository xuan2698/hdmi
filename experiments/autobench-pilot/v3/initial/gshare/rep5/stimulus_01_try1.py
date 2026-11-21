def stimulus(rng, cycles):
    rows = []
    def rv(w): return rng.getrandbits(w)
    def pc(): return rv(7)
    def hist(): return rv(7)
    def row(**kw):
        d = {'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':0,
             'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0}
        d.update(kw)
        return d
    rows.append(row(areset=1))
    rows.append(row(areset=1, predict_valid=1, predict_pc=pc()))
    rows.append(row(areset=0))
    for i in range(6):
        rows.append(row(predict_valid=1, predict_pc=pc()))
    for i in range(4):
        rows.append(row(train_valid=1, train_taken=rv(1), train_mispredicted=rv(1),
                        train_history=hist(), train_pc=pc()))
    rows.append(row(predict_valid=1, predict_pc=pc(), train_valid=1, train_taken=1,
                    train_mispredicted=1, train_history=hist(), train_pc=pc()))
    rows.append(row(predict_valid=1, predict_pc=pc(), train_valid=1, train_taken=0,
                    train_mispredicted=0, train_history=hist(), train_pc=pc()))
    while len(rows) < cycles:
        r = row()
        if rng.random() < 0.6:
            r['predict_valid'] = 1
            r['predict_pc'] = pc()
        if rng.random() < 0.5:
            r['train_valid'] = 1
            r['train_taken'] = rv(1)
            r['train_mispredicted'] = 1 if rng.random() < 0.3 else 0
            r['train_history'] = hist()
            r['train_pc'] = pc()
        if rng.random() < 0.15:
            r['mid'] = {'predict_valid': rv(1), 'predict_pc': pc()}
        rows.append(r)
    return rows[:cycles]
