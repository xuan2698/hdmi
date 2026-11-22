def reference(vectors):
    h=0
    cur={'areset':0,'predict_valid':0,'predict_taken':0,'train_mispredicted':0,'train_taken':0,'train_history':0}
    out=[]
    for v in vectors:
        for k in cur:
            if k in v:
                cur[k]=v[k]
        if cur['areset']:
            h=0
        else:
            if cur['train_mispredicted']:
                h=((cur['train_history'] & 0x7fffffff) << 1) | (cur['train_taken'] & 1)
            elif cur['predict_valid']:
                h=((h & 0x7fffffff) << 1) | (cur['predict_taken'] & 1)
            h &= 0xffffffff
        out.append({'predict_history': h & 0xffffffff})
        if 'mid' in v:
            for k,val in v['mid'].items():
                cur[k]=val
            if cur.get('areset',0):
                h=0
    return out
