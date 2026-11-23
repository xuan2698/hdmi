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
        train_taken = row.get('train_taken', 0) & 1
        train_mispredicted = row.get('train_mispredicted', 0) & 1
        train_history = row.get('train_history', 0) & 0x7f
        train_pc = row.get('train_pc', 0) & 0x7f

        idx_pred = (predict_pc ^ history) & 0x7f
        pred_taken = 1 if pht[idx_pred] >= 2 else 0
        predict_history_out = history
        out.append({'predict_taken': pred_taken, 'predict_history': predict_history_out})

        next_history = history
        if predict_valid:
            next_history = ((history << 1) | pred_taken) & 0x7f
        if train_valid and train_mispredicted:
            next_history = ((train_history << 1) | train_taken) & 0x7f

        if train_valid:
            idx_train = (train_pc ^ train_history) & 0x7f
            if train_taken:
                if pht[idx_train] < 3:
                    pht[idx_train] += 1
            else:
                if pht[idx_train] > 0:
                    pht[idx_train] -= 1

        history = next_history

    return out
