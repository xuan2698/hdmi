def reference(vectors):
    pht = [0] * 128
    ghr = 0
    out = []
    for row in vectors:
        if isinstance(row, dict):
            areset = row.get('areset', 0) & 1
            predict_valid = row.get('predict_valid', 0) & 1
            predict_pc = row.get('predict_pc', 0) & 0x7F
            train_valid = row.get('train_valid', 0) & 1
            train_taken = row.get('train_taken', 0) & 1
            train_mispredicted = row.get('train_mispredicted', 0) & 1
            train_history = row.get('train_history', 0) & 0x7F
            train_pc = row.get('train_pc', 0) & 0x7F
        else:
            areset = row[0] & 1
            predict_valid = row[1] & 1
            predict_pc = row[2] & 0x7F
            train_valid = row[3] & 1
            train_taken = row[4] & 1
            train_mispredicted = row[5] & 1
            train_history = row[6] & 0x7F
            train_pc = row[7] & 0x7F

        if areset:
            pht = [0] * 128
            ghr = 0
            predict_taken = 0
            predict_history = 0
        else:
            idx = (predict_pc ^ ghr) & 0x7F
            predict_taken = 1 if pht[idx] >= 2 else 0
            predict_history = ghr

            new_pht = pht[:]
            if train_valid:
                tidx = (train_pc ^ train_history) & 0x7F
                c = new_pht[tidx]
                if train_taken:
                    if c < 3:
                        c += 1
                else:
                    if c > 0:
                        c -= 1
                new_pht[tidx] = c

            if train_valid and train_mispredicted:
                new_ghr = ((train_history << 1) | train_taken) & 0x7F
            elif predict_valid:
                new_ghr = ((ghr << 1) | predict_taken) & 0x7F
            else:
                new_ghr = ghr

            pht = new_pht
            ghr = new_ghr

        out.append({
            'predict_taken': predict_taken,
            'predict_history': predict_history
        })
    return out
