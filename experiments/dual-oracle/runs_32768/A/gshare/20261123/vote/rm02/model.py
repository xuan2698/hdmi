def reference(vectors):
    ghr = 0
    pht = [0] * 128
    out = []
    for row in vectors:
        areset = row.get('areset', 0)
        if areset:
            ghr = 0
            pht = [0] * 128
            out.append({'predict_taken': 0, 'predict_history': 0})
            continue

        predict_valid = row.get('predict_valid', 0)
        predict_pc = row.get('predict_pc', 0) & 0x7f
        train_valid = row.get('train_valid', 0)
        train_taken = row.get('train_taken', 0) & 1
        train_mispredicted = row.get('train_mispredicted', 0)
        train_history = row.get('train_history', 0) & 0x7f
        train_pc = row.get('train_pc', 0) & 0x7f

        idx = (predict_pc ^ ghr) & 0x7f
        predict_taken = 1 if pht[idx] >= 2 else 0
        predict_history = ghr
        out.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        if train_valid and train_mispredicted:
            next_ghr = ((train_history << 1) & 0x7f) | train_taken
        elif predict_valid:
            next_ghr = ((ghr << 1) & 0x7f) | predict_taken
        else:
            next_ghr = ghr

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

        ghr = next_ghr

    return out
