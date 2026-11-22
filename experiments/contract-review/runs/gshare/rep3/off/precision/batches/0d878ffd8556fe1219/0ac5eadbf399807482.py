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
        # combinational outputs
        if pv:
            idx = (ppc ^ ghr) & 0x7f
            c = pht[idx]
            pt = 1 if c >= 2 else 0
            ph = ghr
        else:
            pt = 0
            ph = 0
        out.append({'predict_taken':pt,'predict_history':ph})
        # sequential updates
        new_ghr = ghr
        if tv:
            tidx = (tpc ^ th) & 0x7f
            c = pht[tidx]
            if tt:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            pht[tidx] = c
            if tm:
                new_ghr = ((th << 1) | tt) & 0x7f
        elif pv:
            new_ghr = ((ghr << 1) | pt) & 0x7f
        ghr = new_ghr
    return out
