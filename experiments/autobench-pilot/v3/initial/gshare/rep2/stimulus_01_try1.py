def stimulus(rng, cycles):
    rows = []
    def rv():
        return rng.getrandbits(1)
    def rp():
        return rng.getrandbits(7)
    def rh():
        return rng.getrandbits(7)
    rows.append({'areset':1,'predict_valid':0,'predict_pc':0,'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0})
    rows.append({'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0})
    for i in range(6):
        rows.append({'areset':0,'predict_valid':1,'predict_pc':rp(),'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0})
    for i in range(6):
        rows.append({'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':1,'train_taken':rv(),'train_mispredicted':0,'train_history':rh(),'train_pc':rp()})
    for i in range(4):
        rows.append({'areset':0,'predict_valid':1,'predict_pc':rp(),'train_valid':1,'train_taken':rv(),'train_mispredicted':1,'train_history':rh(),'train_pc':rp()})
    while len(rows) < cycles:
        pv = rv()
        tv = rv()
        r = {'areset':0,'predict_valid':pv,'predict_pc':rp() if pv else 0,'train_valid':tv,'train_taken':rv() if tv else 0,'train_mispredicted':rv() if tv else 0,'train_history':rh() if tv else 0,'train_pc':rp() if tv else 0}
        if rng.random() < 0.3:
            r['mid'] = {'predict_valid':rv(),'train_valid':rv()}
        rows.append(r)
    return rows[:cycles]
