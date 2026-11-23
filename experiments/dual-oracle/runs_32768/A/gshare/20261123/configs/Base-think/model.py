def reference(vectors):
    g=0
    p=[0]*128
    cur={}
    out=[]
    for row in vectors:
        for k,v in row.items():
            if k!='mid':
                cur[k]=v
        if cur.get('areset',0):
            g=0
            p=[0]*128
        pv=cur.get('predict_valid',0)
        ppc=cur.get('predict_pc',0)&127
        tv=cur.get('train_valid',0)
        tt=cur.get('train_taken',0)&1
        tm=cur.get('train_mispredicted',0)&1
        th=cur.get('train_history',0)&127
        tpc=cur.get('train_pc',0)&127
        pt=(p[(ppc^g)&127]>>1)&1
        ng=g
        if cur.get('areset',0):
            ng=0
        elif tv and tm:
            ng=((th<<1)&127)|tt
        elif pv:
            ng=((g<<1)&127)|pt
        if not cur.get('areset',0) and tv:
            i=(tpc^th)&127
            c=p[i]
            if tt:
                if c<3:
                    c+=1
            else:
                if c>0:
                    c-=1
            p[i]=c
        g=ng
        i=(ppc^g)&127
        out.append({'predict_taken':(p[i]>>1)&1,'predict_history':g})
        if 'mid' in row:
            for k,v in row['mid'].items():
                cur[k]=v
            if cur.get('areset',0):
                g=0
                p=[0]*128
    return out
