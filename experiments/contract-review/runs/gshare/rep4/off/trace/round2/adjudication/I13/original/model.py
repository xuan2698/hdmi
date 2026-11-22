def reference(vectors):
    # State: pht 128 entries of 2-bit counters, ghr 7-bit
    # Initialize to reset state (all zeros)
    pht = [0] * 128
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

        # R6_async_reset: asynchronous active-high reset clears GHR and PHT
        if areset:
            pht = [0] * 128
            ghr = 0
            results.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # R1_predict_outputs: combinational read of PHT and GHR before edge update
        if predict_valid:
            idx = (predict_pc & 0x7F) ^ (ghr & 0x7F)
            counter = pht[idx]
            predict_taken = 1 if counter >= 2 else 0
            predict_history = ghr & 0x7F
        else:
            predict_taken = 0
            predict_history = 0

        results.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Compute next state (posedge updates)
        next_pht = list(pht)
        next_ghr = ghr

        # R3_train_pht_update: train PHT entry toward train_taken (2-bit saturating)
        if train_valid:
            tidx = (train_pc & 0x7F) ^ (train_history & 0x7F)
            c = next_pht[tidx]
            if train_taken:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            next_pht[tidx] = c

        # R4_train_mispredict_ghr_recover / R5_train_precedence_over_predict
        if train_valid and train_mispredicted:
            # GHR restored to train_history shifted with train_taken
            next_ghr = ((train_history << 1) | (train_taken & 1)) & 0x7F
        elif predict_valid:
            # R2_predict_ghr_update: shift in predicted direction
            next_ghr = ((ghr << 1) | (predict_taken & 1)) & 0x7F

        pht = next_pht
        ghr = next_ghr

    return results
