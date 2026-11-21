def stimulus(rng, cycles):
    rows = []
    def rv(): return rng.getrandbits(1)
    def r7(): return rng.randrange(128)
    rows.append({'areset':1,'predict_valid':0,'predict_pc':0,'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0})
    rows.append({'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0})
    for i in range(6):
        rows.append({'areset':0,'predict_valid':1,'predict_pc':r7(),'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0})
    for i in range(4):
        rows.append({'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':1,'train_taken':rv(),'train_mispredicted':0,'train_history':r7(),'train_pc':r7()})
    for i in range(3):
        rows.append({'areset':0,'predict_valid':1,'predict_pc':r7(),'train_valid':1,'train_taken':rv(),'train_mispredicted':1,'train_history':r7(),'train_pc':r7()})
    while len(rows) < cycles:
        pv = rv(); tv = rv()
        rows.append({'areset':0,'predict_valid':pv,'predict_pc':r7() if pv else 0,'train_valid':tv,'train_taken':rv() if tv else 0,'train_mispredicted':rv() if tv else 0,'train_history':r7() if tv else 0,'train_pc':r7() if tv else 0})
    return rows[:cycles]
