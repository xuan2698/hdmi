def reference(vectors):
    pht=[0]*128
    ghr=0
    outs=[]
    for v in vectors:
        if v['areset']:
            pht=[0]*128
            ghr=0
            outs.append({'predict_taken':0,'predict_history':0})
            continue
        pv=v['predict_valid']
        tv=v['train_valid']
        if pv:
            idx=(v['predict_pc']^ghr)&0x7f
            c=pht[idx]
            pt=1 if c>=2 else 0
            ph=ghr
        else:
            pt=0
            ph=0
        outs.append({'predict_taken':pt,'predict_history':ph})
        if tv:
            idx=(v['train_pc']^v['train_history'])&0x7f
            c=pht[idx]
            if v['train_taken']:
                if c<3: c+=1
            else:
                if c>0: c-=1
            pht[idx]=c
        if tv and v['train_mispredicted']:
            ghr=v['train_history']&0x7f
        elif pv:
            ghr=((ghr<<1)|pt)&0x7f
    return outs