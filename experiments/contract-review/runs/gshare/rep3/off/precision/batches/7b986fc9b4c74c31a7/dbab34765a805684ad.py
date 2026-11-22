def reference(vectors):
    pht = [0]*128
    ghr = 0
    out = []
    for v in vectors:
        areset = v['areset']
        if areset:
            pht = [0]*128
            ghr = 0
            out.append({'predict_taken':0,'predict_history':0})
            continue
        pv = v['predict_valid']
        ppc = v['predict_pc']
        tv = v['train_valid']
        tt = v['train_taken']
        tm = v['train_mispredicted']
        th = v['train_history']
        tpc = v['train_pc']
        if pv:
            idx = (ppc ^ ghr) & 0x7f
            c = pht[idx]
            pt = 1 if c >= 2 else 0
            ph = ghr
        else:
            pt = 0
            ph = 0
        out.append({'predict_taken':pt,'predict_history':ph})
        new_pht = list(pht)
        if tv:
            idx = (tpc ^ th) & 0x7f
            new_pht[idx] = 3 if tt else 0
        new_ghr = ghr
        if tv:
            if tm:
                new_ghr = ((th << 1) | tt) & 0x7f
            else:
                new_ghr = ((ghr << 1) | tt) & 0x7f
        elif pv:
            new_ghr = ((ghr << 1) | pt) & 0x7f
        pht = new_pht
        ghr = new_ghr
    return out
