def stimulus(rng, cycles):
    rows = []
    def rv(): return rng.getrandbits(1)
    def r7(): return rng.getrandbits(7)
    rows.append({'areset':1,'predict_valid':0,'predict_pc':0,'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':0,'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':1,'train_valid':1,'train_taken':1,'train_mispredicted':0,'train_history':0,'train_pc':1})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':2,'train_valid':1,'train_taken':0,'train_mispredicted':1,'train_history':1,'train_pc':2})
    rows.append({'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':1,'train_taken':1,'train_mispredicted':1,'train_history':3,'train_pc':3})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':4,'train_valid':1,'train_taken':1,'train_mispredicted':1,'train_history':5,'train_pc':4,'mid':{'predict_valid':0}})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':5,'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0})
    rows.append({'areset':1,'predict_valid':1,'predict_pc':6,'train_valid':1,'train_taken':1,'train_mispredicted':1,'train_history':7,'train_pc':6})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':7,'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0})
    rows.append({'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':1,'train_taken':0,'train_mispredicted':0,'train_history':9,'train_pc':8})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':9,'train_valid':1,'train_taken':0,'train_mispredicted':0,'train_history':11,'train_pc':9})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':10,'train_valid':1,'train_taken':1,'train_mispredicted':0,'train_history':13,'train_pc':10})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':11,'train_valid':1,'train_taken':0,'train_mispredicted':1,'train_history':15,'train_pc':11})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':12,'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0})
    rows.append({'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':1,'train_taken':1,'train_mispredicted':1,'train_history':17,'train_pc':12})
    rows.append({'areset':0,'predict_valid':1,'predict_pc':13,'train_valid':1,'train_taken':1,'train_mispredicted':1,'train_history':19,'train_pc':13})
    while len(rows) < cycles:
        pv = rv()
        tv = rv()
        tm = rv() if tv else 0
        rows.append({
            'areset': 1 if rng.random() < 0.02 else 0,
            'predict_valid': pv,
            'predict_pc': r7() if pv else 0,
            'train_valid': tv,
            'train_taken': rv() if tv else 0,
            'train_mispredicted': tm,
            'train_history': r7() if tv else 0,
            'train_pc': r7() if tv else 0,
        })
    return rows[:cycles]
