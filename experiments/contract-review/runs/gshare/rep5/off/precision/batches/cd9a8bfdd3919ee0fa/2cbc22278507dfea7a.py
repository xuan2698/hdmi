def reference(vectors):
    pht = [0]*128
    ghr = 0
    out = []
    for v in vectors:
        if v['areset']:
            pht = [0]*128
            ghr = 0
            out.append({'predict_taken':0,'predict_history':0})
            continue
        pv = v['predict_valid']
        tv = v['train_valid']
        ppc = v['predict_pc']
        tpc = v['train_pc']
        th = v['train_history']
        tt = v['train_taken']
        tm = v['train_mispredicted']
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
            c = new_pht[idx]
            if tt:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            new_pht[idx] = c
        if tv:
            if tm:
                new_ghr = ((th << 1) | tt) & 0x7f
            else:
                new_ghr = ghr
        elif pv:
            new_ghr = ((ghr << 1) | pt) & 0x7f
        else:
            new_ghr = ghr
        pht = new_pht
        ghr = new_ghr
    return out
