def reference(vectors):
    ghr = 0
    pht = [0] * 128
    outs = []
    for row in vectors:
        if isinstance(row, dict):
            areset = int(row.get('areset', 0)) & 1
            predict_valid = int(row.get('predict_valid', 0)) & 1
            predict_pc = int(row.get('predict_pc', 0)) & 0x7F
            train_valid = int(row.get('train_valid', 0)) & 1
            train_taken = int(row.get('train_taken', 0)) & 1
            train_mispredicted = int(row.get('train_mispredicted', 0)) & 1
            train_history = int(row.get('train_history', 0)) & 0x7F
            train_pc = int(row.get('train_pc', 0)) & 0x7F
        else:
            L = len(row)
            if L == 9:
                areset = int(row[1]) & 1
                predict_valid = int(row[2]) & 1
                predict_pc = int(row[3]) & 0x7F
                train_valid = int(row[4]) & 1
                train_taken = int(row[5]) & 1
                train_mispredicted = int(row[6]) & 1
                train_history = int(row[7]) & 0x7F
                train_pc = int(row[8]) & 0x7F
            elif L == 8:
                areset = int(row[0]) & 1
                predict_valid = int(row[1]) & 1
                predict_pc = int(row[2]) & 0x7F
                train_valid = int(row[3]) & 1
                train_taken = int(row[4]) & 1
                train_mispredicted = int(row[5]) & 1
                train_history = int(row[6]) & 0x7F
                train_pc = int(row[7]) & 0x7F
            else:
                vals = list(row) + [0] * 9
                areset = int(vals[1]) & 1
                predict_valid = int(vals[2]) & 1
                predict_pc = int(vals[3]) & 0x7F
                train_valid = int(vals[4]) & 1
                train_taken = int(vals[5]) & 1
                train_mispredicted = int(vals[6]) & 1
                train_history = int(vals[7]) & 0x7F
                train_pc = int(vals[8]) & 0x7F
        if areset:
            ghr = 0
            pht = [0] * 128
        pidx = (predict_pc ^ ghr) & 0x7F
        pred = 1 if pht[pidx] >= 2 else 0
        outs.append({'predict_taken': pred, 'predict_history': ghr})
        if areset:
            continue
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
            ghr = ((ghr << 1) | pred) & 0x7F
    return outs
