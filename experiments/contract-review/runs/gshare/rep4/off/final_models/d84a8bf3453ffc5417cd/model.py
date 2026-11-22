def reference(vectors):
    # Contract implementation.
    # State: ghr (7-bit), pht (128 entries of 2-bit counters).
    # Reset is async active-high. PHT reset value unspecified; choose all 2'b00.
    # R6_async_reset: areset clears GHR and PHT asynchronously.
    # R1_predict_outputs: combinational read of PHT and GHR when predict_valid.
    # R2_predict_ghr_update: predict_valid & !train_valid -> GHR shifts in predicted dir at posedge.
    # R3_train_pht_update: train_valid -> PHT entry updated toward train_taken at posedge.
    # R4_train_mispredict_ghr_recover: train_valid & train_mispredicted -> GHR = train_history at posedge.
    # R5_train_precedence_over_predict: mispredict training wins over prediction GHR shift.

    # Initialize state (power-up unspecified; use zeros)
    ghr = 0
    pht = [0] * 128  # 2-bit counters, reset value 0

    results = []

    for row in vectors:
        areset = row.get('areset', 0)
        predict_valid = row.get('predict_valid', 0)
        predict_pc = row.get('predict_pc', 0) & 0x7F
        train_valid = row.get('train_valid', 0)
        train_taken = row.get('train_taken', 0)
        train_mispredicted = row.get('train_mispredicted', 0)
        train_history = row.get('train_history', 0) & 0x7F
        train_pc = row.get('train_pc', 0) & 0x7F

        # R6_async_reset: async reset clears state immediately
        if areset:
            ghr = 0
            pht = [0] * 128
            results.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # R1_predict_outputs: combinational read
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
        new_ghr = ghr
        new_pht = list(pht)

        # R3_train_pht_update: update PHT entry toward train_taken
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

        # R4_train_mispredict_ghr_recover and R5_train_precedence_over_predict
        if train_valid and train_mispredicted:
            # Training recovery takes precedence over prediction GHR update
            new_ghr = train_history
        elif predict_valid and not train_valid:
            # R2_predict_ghr_update: shift in predicted direction
            new_ghr = ((ghr << 1) | predict_taken) & 0x7F
        # else: no GHR change (train_valid without mispredict, or nothing)

        ghr = new_ghr
        pht = new_pht

    return results
