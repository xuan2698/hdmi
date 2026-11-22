def reference(vectors):
    ghr=0; pht=[0]*128
    inp={'areset':0,'predict_valid':0,'predict_pc':0,'train_valid':0,'train_taken':0,'train_mispredicted':0,'train_history':0,'train_pc':0}
    res=[]
    for row in vectors:
        for k,v in row.items():
            if k!='mid': inp[k]=v&(0x7F if k in ('predict_pc','train_history','train_pc') else 1)
        if inp['areset']:
            ghr=0; pht=[0]*128
        pt=0; ph=0
        if inp['predict_valid']:
            ph=ghr
            idx=(inp['predict_pc']^ghr)&0x7F
            pt=1 if pht[idx]>=2 else 0
        res.append({'predict_taken':pt,'predict_history':ph})
        if not inp['areset']:
            if inp['train_valid']:
                idx=(inp['train_pc']^inp['train_history'])&0x7F
                c=pht[idx]
                if inp['train_taken']:
                    if c<3: c+=1
                else:
                    if c>0: c-=1
                pht[idx]=c
            if inp['train_valid'] and inp['train_mispredicted']:
                ghr=((inp['train_history']<<1)|inp['train_taken'])&0x7F
            elif inp['predict_valid']:
                ghr=((ghr<<1)|pt)&0x7F
        mid=row.get('mid',{})
        for k,v in mid.items():
            inp[k]=v&(0x7F if k in ('predict_pc','train_history','train_pc') else 1)
        if inp['areset']:
            ghr=0; pht=[0]*128
    return res
