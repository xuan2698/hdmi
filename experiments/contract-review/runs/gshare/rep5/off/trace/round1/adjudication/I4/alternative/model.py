def reference(vectors):
    # State
    pht = [2] * 128  # R1_predict_outputs: PHT counters reset to 2 (weakly not-taken)
    ghr = 0

    results = []

    for vec in vectors:
        areset = vec.get('areset', 0)
        predict_valid = vec.get('predict_valid', 0)
        predict_pc = vec.get('predict_pc', 0)
        train_valid = vec.get('train_valid', 0)
        train_taken = vec.get('train_taken', 0)
        train_mispredicted = vec.get('train_mispredicted', 0)
        train_history = vec.get('train_history', 0)
        train_pc = vec.get('train_pc', 0)

        # R7_async_reset: asynchronous active-high reset
        if areset:
            pht = [2] * 128
            ghr = 0
            results.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # R1_predict_outputs: produce prediction using current PHT and GHR
        # R6_predict_sees_pre_train_pht: prediction sees PHT before training update
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            counter = pht[idx]
            predict_taken = 1 if counter >= 2 else 0
            predict_history = ghr
        else:
            predict_taken = 0
            predict_history = 0

        results.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Compute next state (posedge updates)
        new_pht = list(pht)
        new_ghr = ghr

        # R3_train_pht_update: train PHT
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

        # R4_train_mispredict_ghr_recover: recover GHR on mispredict
        # R5_train_priority_over_predict_ghr: training takes precedence over prediction for GHR
        if train_valid:
            if train_mispredicted:
                new_ghr = (train_history << 1 | train_taken) & 0x7F
            else:
                new_ghr = (train_history << 1 | train_taken) & 0x7F
        elif predict_valid:
            # R2_predict_ghr_update: update GHR for predicted branch
            new_ghr = ((ghr << 1) | predict_taken) & 0x7F

        pht = new_pht
        ghr = new_ghr

    return results
