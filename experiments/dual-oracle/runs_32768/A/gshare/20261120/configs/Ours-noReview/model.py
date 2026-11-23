def reference(vectors):
    pht = [0] * 128
    history = 0
    out = []
    for row in vectors:
        areset = row.get('areset', 0)
        if areset:
            pht = [0] * 128
            history = 0

        pv = row.get('predict_valid', 0)
        ppc = row.get('predict_pc', 0) & 0x7f
        idx = (ppc ^ history) & 0x7f
        c = pht[idx]
        pred_taken = 1 if c >= 2 else 0
        pred_hist = history & 0x7f
        out.append({'predict_taken': pred_taken, 'predict_history': pred_hist})

        if areset:
            continue

        tv = row.get('train_valid', 0)
        tt = row.get('train_taken', 0) & 1
        tm = row.get('train_mispredicted', 0)
        th = row.get('train_history', 0) & 0x7f
        tpc = row.get('train_pc', 0) & 0x7f

        if tv:
            tidx = (tpc ^ th) & 0x7f
            pcnt = pht[tidx]
            if tt:
                if pcnt < 3:
                    pht[tidx] = pcnt + 1
            else:
                if pcnt > 0:
                    pht[tidx] = pcnt - 1

        if tv and tm:
            history = ((th << 1) | tt) & 0x7f
        elif pv:
            history = ((history << 1) | pred_taken) & 0x7f

    return out
