def reference(vectors):
    # State
    ghr = 0
    pht = [0] * 128  # 2-bit saturating counters, reset to 0

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

        # R8_async_reset: asynchronous active-high reset
        if areset:
            ghr = 0
            pht = [0] * 128
            results.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # R1_predict_outputs / R2_predict_no_valid: combinational prediction
        # R7_predict_sees_pre_train_pht: prediction uses current PHT (before training edge)
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            counter = pht[idx]
            predict_taken = 1 if counter >= 2 else 0
            predict_history = ghr & 0x7F
        else:
            # R2: assumed zero when no prediction requested
            predict_taken = 0
            predict_history = 0

        results.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Compute next-state updates (posedge)
        new_ghr = ghr
        new_pht = list(pht)

        # R4_train_pht_update: update PHT on training
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

        # R5_train_mispredict_ghr_recover / R6_train_priority_over_predict_ghr
        if train_valid and train_mispredicted:
            new_ghr = train_history & 0x7F
        elif predict_valid:
            # R3_ghr_update_predict: shift in predicted direction
            new_ghr = ((ghr << 1) | predict_taken) & 0x7F

        ghr = new_ghr
        pht = new_pht

    return results
