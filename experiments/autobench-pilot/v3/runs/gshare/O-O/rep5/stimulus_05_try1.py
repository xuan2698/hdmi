def stimulus(rng, cycles):
    rows = []
    def rv(w): return rng.getrandbits(w)
    def row(**kw):
        d = {'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':0,
             'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0}
        d.update(kw)
        rows.append(d)
    row(areset=1)
    row(areset=1)
    row()
    for i in range(cycles-3):
        d = {'areset':0,
             'predict_valid': rng.choice([0,1,1]),
             'predict_pc': rv(7),
             'train_valid': rng.choice([0,1,1]),
             'train_taken': rv(1),
             'train_mispredicted': rng.choice([0,0,1]),
             'train_history': rv(7),
             'train_pc': rv(7)}
        if rng.random() < 0.3:
            d['mid'] = {'predict_valid': rv(1), 'train_valid': rv(1),
                        'train_mispredicted': rv(1), 'train_history': rv(7),
                        'predict_pc': rv(7), 'train_pc': rv(7),
                        'train_taken': rv(1)}
        rows.append(d)
    return rows[:cycles]
