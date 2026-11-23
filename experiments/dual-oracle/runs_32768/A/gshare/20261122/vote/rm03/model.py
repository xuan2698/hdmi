def reference(vectors):
    history = 0
    pht = [0] * 128
    out = []
    for row in vectors:
        areset = row.get('areset', 0)
        if areset:
            history = 0
            pht = [0] * 128
            out.append({'predict_taken': 0, 'predict_history': 0})
            continue

        predict_valid = row.get('predict_valid', 0)
        predict_pc = row.get('predict_pc', 0) & 0x7f
        train_valid = row.get('train_valid', 0)
        train_taken = row.get('train_taken', 0) & 0x1
        train_mispredicted = row.get('train_mispredicted', 0)
        train_history = row.get('train_history', 0) & 0x7f
        train_pc = row.get('train_pc', 0) & 0x7f

        idx = (predict_pc ^ history) & 0x7f
        pred_cnt = pht[idx]
        pred_taken = (pred_cnt >> 1) & 0x1
        pred_history = history

        next_history = history
        if train_valid and train_mispredicted:
            next_history = ((train_history << 1) | train_taken) & 0x7f
        elif predict_valid:
            next_history = ((history << 1) | pred_taken) & 0x7f

        if train_valid:
            tidx = (train_pc ^ train_history) & 0x7f
            cnt = pht[tidx]
            if train_taken:
                if cnt < 3:
                    cnt += 1
            else:
                if cnt > 0:
                    cnt -= 1
            pht[tidx] = cnt

        history = next_history
        out.append({'predict_taken': pred_taken, 'predict_history': pred_history})
    return out
