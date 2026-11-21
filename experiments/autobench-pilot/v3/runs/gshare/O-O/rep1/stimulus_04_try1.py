def stimulus(rng, cycles):
    rows = []
    def rv():
        return {
            'areset': 0,
            'predict_valid': rng.getrandbits(1),
            'predict_pc': rng.getrandbits(7),
            'train_valid': rng.getrandbits(1),
            'train_taken': rng.getrandbits(1),
            'train_mispredicted': rng.getrandbits(1),
            'train_history': rng.getrandbits(7),
            'train_pc': rng.getrandbits(7),
        }
    rows.append({'areset':1,'predict_valid':0,'predict_pc':0,'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0})
    rows.append({'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0})
    for i in range(4):
        r = rv()
        r['predict_valid'] = 1
        r['train_valid'] = 0
        rows.append(r)
    for i in range(3):
        r = rv()
        r['predict_valid'] = 0
        r['train_valid'] = 1
        rows.append(r)
    for i in range(3):
        r = rv()
        r['predict_valid'] = 1
        r['train_valid'] = 1
        r['train_mispredicted'] = 1
        rows.append(r)
    for i in range(2):
        r = rv()
        r['predict_valid'] = 1
        r['train_valid'] = 1
        r['train_mispredicted'] = 0
        rows.append(r)
    while len(rows) < cycles:
        r = rv()
        if rng.random() < 0.3:
            r['predict_valid'] = 1
        if rng.random() < 0.3:
            r['train_valid'] = 1
        if rng.random() < 0.2:
            r['train_mispredicted'] = 1
        rows.append(r)
    return rows[:cycles]
