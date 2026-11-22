def reference(vectors):
    pht=[1]*128
    ghr=0
    out=[]
    for v in vectors:
        if v['areset']:
            pht=[1]*128
            ghr=0
            out.append({'predict_taken':0,'predict_history':0})
            continue
        pt=0
        ph=0
        if v['predict_valid']:
            idx=(v['predict_pc']^ghr)&0x7f
            pt=1 if pht[idx]>=2 else 0
            ph=ghr
        out.append({'predict_taken':pt,'predict_history':ph})
        if v['train_valid']:
            idx=(v['train_pc']^v['train_history'])&0x7f
            c=pht[idx]
            if v['train_taken']:
                if c<3: c+=1
            else:
                if c>0: c-=1
            pht[idx]=c
        if v['train_valid'] and v['train_mispredicted']:
            ghr=v['train_history']&0x7f
        elif v['predict_valid']:
            ghr=((ghr<<1)|pt)&0x7f
    return out
