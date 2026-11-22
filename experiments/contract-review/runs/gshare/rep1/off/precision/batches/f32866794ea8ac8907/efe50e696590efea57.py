def reference(vectors):
    ghr = 0
    pht = [0]*128
    out = []
    for v in vectors:
        areset = v['areset']
        if areset:
            ghr = 0
            pht = [0]*128
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
        new_ghr = ghr
        if tv:
            idx = (tpc ^ th) & 0x7f
            c = pht[idx]
            if tt:
                if c < 3:
                    pht[idx] = c+1
            else:
                if c > 0:
                    pht[idx] = c-1
            if tm:
                new_ghr = th
            elif pv:
                new_ghr = ((ghr << 1) | pt) & 0x7f
        elif pv:
            new_ghr = ((ghr << 1) | pt) & 0x7f
        ghr = new_ghr
    return out
