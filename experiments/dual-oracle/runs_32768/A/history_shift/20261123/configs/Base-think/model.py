def reference(vectors):
    m=(1<<32)-1
    s=0
    c={}
    o=[]
    for r in vectors:
        for k,v in r.items():
            if k!='mid' and k!='clk':
                c[k]=v
        if c.get('areset',0):
            s=0
        elif c.get('train_mispredicted',0):
            s=(((c.get('train_history',0)&m)<<1)|(c.get('train_taken',0)&1))&m
        elif c.get('predict_valid',0):
            s=((s<<1)|(c.get('predict_taken',0)&1))&m
        o.append({'predict_history':s})
        for k,v in r.get('mid',{}).items():
            if k!='clk':
                c[k]=v
                if k=='areset' and v:
                    s=0
    return o
