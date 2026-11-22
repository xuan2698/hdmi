def reference(vectors):
    m=(1<<32)-1
    s=0
    r=[]
    for v in vectors:
        if v.get('areset',0):
            s=0
        elif v.get('train_mispredicted',0):
            s=((v.get('train_history',0)<<1)|v.get('train_taken',0))&m
        elif v.get('predict_valid',0):
            s=((s<<1)|v.get('predict_taken',0))&m
        r.append({'predict_history':s&m})
        x=v.get('mid')
        if x and x.get('areset',0):
            s=0
    return r
