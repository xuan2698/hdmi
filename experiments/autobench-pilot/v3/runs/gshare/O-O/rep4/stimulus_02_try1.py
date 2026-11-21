def stimulus(rng, cycles):
    rows = []
    def rv(w): return rng.getrandbits(w)
    def pc(): return rv(7)
    def hist(): return rv(7)
    rows.append({'areset':1,'predict_valid':0,'predict_pc':0,'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':pc(),'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':pc(),'train_valid':1,'train_taken':1,'train_mispredicted':0,'train_history':hist(),'train_pc':pc()})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':pc(),'train_valid':1,'train_taken':0,'train_mispredicted':1,'train_history':hist(),'train_pc':pc()})
    rows.append({'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':1,'train_taken':1,'train_mispredicted':1,'train_history':hist(),'train_pc':pc()})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':pc(),'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':pc(),'train_valid':1,'train_taken':1,'train_mispredicted':0,'train_history':hist(),'train_pc':pc()})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':pc(),'train_valid':1,'train_taken':0,'train_mispredicted':1,'train_history':hist(),'train_pc':pc()})
    rows.append({'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':1,'train_taken':1,'train_mispredicted':0,'train_history':hist(),'train_pc':pc()})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':pc(),'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':pc(),'train_valid':1,'train_taken':1,'train_mispredicted':1,'train_history':hist(),'train_pc':pc()})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':pc(),'train_valid':1,'train_taken':0,'train_mispredicted':0,'train_history':hist(),'train_pc':pc()})
    rows.append({'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':1,'train_taken':0,'train_mispredicted':1,'train_history':hist(),'train_pc':pc()})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':pc(),'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':pc(),'train_valid':1,'train_taken':1,'train_mispredicted':0,'train_history':hist(),'train_pc':pc()})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':pc(),'train_valid':1,'train_taken':0,'train_mispredicted':1,'train_history':hist(),'train_pc':pc()})
    while len(rows) < cycles:
        pv = rng.choice([0,1])
        tv = rng.choice([0,1])
        tm = rng.choice([0,1]) if tv else 0
        tt = rng.choice([0,1]) if tv else 0
        r = {'areset':0,'predict_valid':pv,'predict_pc':pc() if pv else 0,
             'train_valid':tv,'train_taken':tt,'train_mispredicted':tm,
             'train_history':hist() if tv else 0,'train_pc':pc() if tv else 0}
        if rng.random() < 0.3:
            r['mid'] = {'predict_valid':rng.choice([0,1]),'train_valid':rng.choice([0,1])}
        rows.append(r)
    return rows[:cycles]
