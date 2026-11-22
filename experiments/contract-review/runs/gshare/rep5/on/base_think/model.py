def reference(vectors):
    pht=[0]*128
    hist=0
    cur={'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0}
    out=[]
    for row in vectors:
        for k,v in row.items():
            if k!='mid':
                cur[k]=v
        if cur.get('areset',0):
            hist=0
        pc=cur.get('predict_pc',0)&127
        idx=(pc^hist)&127
        pt=(pht[idx]>>1)&1
        out.append({'predict_taken':pt,'predict_history':hist&127})
        if cur.get('train_valid',0):
            ti=((cur.get('train_pc',0)&127)^(cur.get('train_history',0)&127))&127
            if cur.get('train_taken',0):
                if pht[ti]<3:
                    pht[ti]+=1
            else:
                if pht[ti]>0:
                    pht[ti]-=1
        if cur.get('areset',0):
            hist=0
        elif cur.get('train_valid',0) and cur.get('train_mispredicted',0):
            hist=(((cur.get('train_history',0)&127)<<1)|(cur.get('train_taken',0)&1))&127
        elif cur.get('predict_valid',0):
            hist=((hist<<1)|pt)&127
        if 'mid' in row:
            for k,v in row['mid'].items():
                cur[k]=v
            if cur.get('areset',0):
                hist=0
    return out
