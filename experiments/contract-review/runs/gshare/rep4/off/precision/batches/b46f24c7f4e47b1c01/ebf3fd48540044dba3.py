def reference(vectors):
    PHT_INIT = 0
    ghr = 0
    pht = [PHT_INIT] * 128
    out = []
    for v in vectors:
        areset = v.get('areset', 0)
        if areset:
            ghr = 0
            pht = [PHT_INIT] * 128
            out.append({'predict_taken': 0, 'predict_history': 0})
            continue
        pv = v.get('predict_valid', 0)
        ppc = v.get('predict_pc', 0)
        tv = v.get('train_valid', 0)
        tt = v.get('train_taken', 0)
        tm = v.get('train_mispredicted', 0)
        th = v.get('train_history', 0)
        tpc = v.get('train_pc', 0)
        if pv:
            idx = (ppc ^ ghr) & 0x7F
            c = pht[idx]
            pt = 1 if c >= 2 else 0
            ph = ghr
        else:
            pt = 0
            ph = 0
        out.append({'predict_taken': pt, 'predict_history': ph})
        if tv:
            idx = (tpc ^ th) & 0x7F
            c = pht[idx]
            if tt:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            pht[idx] = c
        if tv and tm:
            ghr = th & 0x7F
        elif pv and not tv:
            ghr = ((ghr << 1) | pt) & 0x7F
    return out
