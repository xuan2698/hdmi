def reference(vectors):
    pht = [0] * 128
    ghr = 0
    out = []
    for v in vectors:
        areset = v.get('areset', 0)
        if areset:
            pht = [0] * 128
            ghr = 0
            out.append({'predict_taken': 0, 'predict_history': 0})
            continue

        predict_valid = v.get('predict_valid', 0) & 1
        predict_pc = v.get('predict_pc', 0) & 0x7f
        train_valid = v.get('train_valid', 0) & 1
        train_taken = v.get('train_taken', 0) & 1
        train_mispredicted = v.get('train_mispredicted', 0) & 1
        train_history = v.get('train_history', 0) & 0x7f
        train_pc = v.get('train_pc', 0) & 0x7f

        idx = (predict_pc ^ ghr) & 0x7f
        ctr = pht[idx]
        pred_taken = 1 if ctr >= 2 else 0
        out.append({'predict_taken': pred_taken, 'predict_history': ghr})

        if train_valid:
            tidx = (train_pc ^ train_history) & 0x7f
            c = pht[tidx]
            if train_taken:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            pht[tidx] = c

        if train_valid and train_mispredicted:
            ghr = ((train_history << 1) | train_taken) & 0x7f
        elif predict_valid:
            ghr = ((ghr << 1) | pred_taken) & 0x7f

    return out
