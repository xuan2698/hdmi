def reference(vectors):
    hist = 0
    pht = [0] * 128
    out_taken = 0
    out_hist = 0
    results = []

    for v in vectors:
        areset = v.get('areset', 0)
        predict_valid = v.get('predict_valid', 0)
        predict_pc = v.get('predict_pc', 0)
        train_valid = v.get('train_valid', 0)
        train_taken = v.get('train_taken', 0)
        train_mispredicted = v.get('train_mispredicted', 0)
        train_history = v.get('train_history', 0)
        train_pc = v.get('train_pc', 0)

        if areset:
            hist = 0
            pht = [0] * 128
            out_taken = 0
            out_hist = 0
            results.append({'predict_taken': out_taken, 'predict_history': out_hist})
            continue

        # Prediction using current (pre-edge) state
        pred_index = (predict_pc ^ hist) & 0x7F
        pred_counter = pht[pred_index]
        pred_taken = 1 if pred_counter >= 2 else 0
        used_hist = hist

        # PHT training update
        new_pht = pht[:]
        if train_valid:
            train_index = (train_pc ^ train_history) & 0x7F
            counter = new_pht[train_index]
            if train_taken:
                if counter < 3:
                    counter += 1
            else:
                if counter > 0:
                    counter -= 1
            new_pht[train_index] = counter

        # History register update (training misprediction has priority)
        if train_valid and train_mispredicted:
            new_hist = ((train_history << 1) & 0x7F) | (train_taken & 1)
        elif predict_valid:
            new_hist = ((hist << 1) & 0x7F) | (pred_taken & 1)
        else:
            new_hist = hist

        # Output registers update
        if predict_valid:
            new_out_taken = pred_taken
            new_out_hist = used_hist
        else:
            new_out_taken = out_taken
            new_out_hist = out_hist

        # Commit state
        hist = new_hist
        pht = new_pht
        out_taken = new_out_taken
        out_hist = new_out_hist

        results.append({'predict_taken': out_taken, 'predict_history': out_hist})

    return results
