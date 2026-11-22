def reference(vectors):
    pht = [0]*128
    ghr = 0
    out = []
    for v in vectors:
        areset = v['areset']
        pv = v['predict_valid']
        ppc = v['predict_pc']
        tv = v['train_valid']
        tt = v['train_taken']
        tm = v['train_mispredicted']
        th = v['train_history']
        tpc = v['train_pc']
        if areset:
            pht = [0]*128
            ghr = 0
            out.append({'predict_taken':0,'predict_history':0})
            continue
        pt = 0
        ph = 0
        if pv:
            idx = (ppc ^ ghr) & 0x7f
            c = pht[idx]
            pt = (c >> 1) & 1
            ph = ghr
        out.append({'predict_taken':pt,'predict_history':ph})
        if tv:
            idx = (tpc ^ th) & 0x7f
            c = pht[idx]
            if tt:
                if c < 3: c += 1
            else:
                if c > 0: c -= 1
            pht[idx] = c
            if tm:
                ghr = ((th << 1) | tt) & 0x7f
        elif pv:
            ghr = ((ghr << 1) | pt) & 0x7f
    return out
