def reference(vectors):
    pht = [0] * 128
    ghr = 0
    out = []

    for row in vectors:
        if isinstance(row, dict):
            areset = row.get('areset', 0)
            predict_valid = row.get('predict_valid', 0)
            predict_pc = row.get('predict_pc', 0) & 0x7F
            train_valid = row.get('train_valid', 0)
            train_taken = row.get('train_taken', 0) & 1
            train_mispredicted = row.get('train_mispredicted', 0) & 1
            train_history = row.get('train_history', 0) & 0x7F
            train_pc = row.get('train_pc', 0) & 0x7F
        else:
            vals = row
            areset = vals[0] if len(vals) > 0 else 0
            predict_valid = vals[1] if len(vals) > 1 else 0
            predict_pc = (vals[2] if len(vals) > 2 else 0) & 0x7F
            train_valid = vals[3] if len(vals) > 3 else 0
            train_taken = (vals[4] if len(vals) > 4 else 0) & 1
            train_mispredicted = (vals[5] if len(vals) > 5 else 0) & 1
            train_history = (vals[6] if len(vals) > 6 else 0) & 0x7F
            train_pc = (vals[7] if len(vals) > 7 else 0) & 0x7F

        if areset:
            pht = [0] * 128
            ghr = 0

        idx = (predict_pc ^ ghr) & 0x7F
        predict_taken = (pht[idx] >> 1) & 1
        predict_history = ghr & 0x7F

        if not areset:
            if train_valid:
                tidx = (train_pc ^ train_history) & 0x7F
                cnt = pht[tidx]
                if train_taken:
                    if cnt < 3:
                        cnt += 1
                else:
                    if cnt > 0:
                        cnt -= 1
                pht[tidx] = cnt

            if train_valid and train_mispredicted:
                ghr = (((train_history & 0x3F) << 1) | train_taken) & 0x7F
            elif predict_valid:
                ghr = (((ghr & 0x3F) << 1) | predict_taken) & 0x7F

        out.append({
            'predict_taken': int(predict_taken),
            'predict_history': int(predict_history)
        })

    return out
