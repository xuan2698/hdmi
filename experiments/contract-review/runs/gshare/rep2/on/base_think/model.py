def reference(vectors):
    h=0
    p=[0]*128
    o=[]
    c={'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0}
    for r in vectors:
        for k in c:
            if k in r:
                c[k]=r[k]
        if c['areset']:
            h=0
            p=[0]*128
        idx=(c['predict_pc']^h)&127
        pt=1 if p[idx]>=2 else 0
        o.append({'predict_taken':pt,'predict_history':h&127})
        if not c['areset']:
            if c['train_valid']:
                i=(c['train_pc']^c['train_history'])&127
                v=p[i]
                if c['train_taken']:
                    if v<3:
                        p[i]=v+1
                elif v>0:
                    p[i]=v-1
            if c['train_valid'] and c['train_mispredicted']:
                h=((c['train_history']<<1)|c['train_taken'])&127
            elif c['predict_valid']:
                h=((h<<1)|pt)&127
        if 'mid' in r:
            for k,v in r['mid'].items():
                c[k]=v
            if c['areset']:
                h=0
                p=[0]*128
    return o
