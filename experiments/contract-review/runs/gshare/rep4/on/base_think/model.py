def reference(vectors):
    h=0
    p=[0]*128
    ci={'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0}
    r=[]
    for row in vectors:
        for k,v in row.items():
            if k!='mid':
                ci[k]=v
        if ci['areset']:
            h=0
            p=[0]*128
        idx=(ci['predict_pc']^h)&0x7f
        pt=(p[idx]>>1)&1
        r.append({'predict_taken':pt,'predict_history':h})
        if not ci['areset']:
            if ci['train_valid']:
                ti=(ci['train_pc']^ci['train_history'])&0x7f
                c=p[ti]
                if ci['train_taken']:
                    if c<3:
                        c+=1
                else:
                    if c>0:
                        c-=1
                p[ti]=c
            if ci['train_valid'] and ci['train_mispredicted']:
                h=((ci['train_history']<<1)|ci['train_taken'])&0x7f
            elif ci['predict_valid']:
                h=((h<<1)|pt)&0x7f
        if 'mid' in row:
            for k,v in row['mid'].items():
                ci[k]=v
                if k=='areset' and v:
                    h=0
                    p=[0]*128
    return r
