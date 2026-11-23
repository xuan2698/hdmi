def reference(vectors):
    ghr = 0
    pht = [0] * 128
    out = []
    for row in vectors:
        if isinstance(row, dict):
            areset = row.get('areset', 0)
            predict_valid = row.get('predict_valid', 0)
            predict_pc = row.get('predict_pc', 0)
            train_valid = row.get('train_valid', 0)
            train_taken = row.get('train_taken', 0)
            train_mispredicted = row.get('train_mispredicted', 0)
            train_history = row.get('train_history', 0)
            train_pc = row.get('train_pc', 0)
        else:
            areset, predict_valid, predict_pc, train_valid, train_taken, train_mispredicted, train_history, train_pc = row
        if areset:
            ghr = 0
            pht = [0] * 128
        idx = (predict_pc ^ ghr) & 0x7F
        counter = pht[idx]
        predict_taken = 1 if counter >= 2 else 0
        predict_history = ghr & 0x7F
        out.append({'predict_taken': predict_taken, 'predict_history': predict_history})
        if not areset:
            if train_valid:
                tidx = (train_pc ^ train_history) & 0x7F
                c = pht[tidx]
                if train_taken:
                    if c < 3:
                        c += 1
                else:
                    if c > 0:
                        c -= 1
                pht[tidx] = c
            if train_valid and train_mispredicted:
                ghr = ((train_history << 1) | train_taken) & 0x7F
            elif predict_valid:
                ghr = ((ghr << 1) | predict_taken) & 0x7F
    return out
