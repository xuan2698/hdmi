def reference(vectors):
    history = 0
    pht = [0] * 128
    outputs = []
    for row in vectors:
        areset = row['areset']
        predict_valid = row['predict_valid']
        predict_pc = row['predict_pc'] & 0x7F
        train_valid = row['train_valid']
        train_taken = row['train_taken']
        train_mispredicted = row['train_mispredicted']
        train_history = row['train_history'] & 0x7F
        train_pc = row['train_pc'] & 0x7F

        if areset:
            history = 0
            pht = [0] * 128
            outputs.append({'predict_taken': 0, 'predict_history': 0})
        else:
            idx_pred = (predict_pc ^ history) & 0x7F
            counter = pht[idx_pred]
            pred_taken = 1 if counter >= 2 else 0
            pred_history = history

            if train_valid:
                idx_train = (train_pc ^ train_history) & 0x7F
                c = pht[idx_train]
                if train_taken:
                    if c < 3:
                        pht[idx_train] = c + 1
                else:
                    if c > 0:
                        pht[idx_train] = c - 1

            if train_valid and train_mispredicted:
                history = ((train_history << 1) | train_taken) & 0x7F
            elif predict_valid:
                history = ((history << 1) | pred_taken) & 0x7F

            outputs.append({'predict_taken': pred_taken, 'predict_history': pred_history})
    return outputs
