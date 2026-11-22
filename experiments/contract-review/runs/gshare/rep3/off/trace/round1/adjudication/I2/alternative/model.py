def reference(vectors):
    # State: pht (128 entries of 2-bit counters), ghr (7-bit)
    # Reset is async active-high.
    pht = [0] * 128
    ghr = 0

    def idx(pc, hist):
        return (pc ^ hist) & 0x7F

    def predict_taken_of(pc, hist):
        # R1_predict_outputs, R6_predict_sees_pre_train_pht
        c = pht[idx(pc, hist)]
        return 1 if c >= 2 else 0

    def sat_update(c, taken):
        if taken:
            return c + 1 if c < 3 else 3
        else:
            return c - 1 if c > 0 else 0

    results = []
    for row in vectors:
        areset = row['areset']
        predict_valid = row['predict_valid']
        predict_pc = row['predict_pc']
        train_valid = row['train_valid']
        train_taken = row['train_taken']
        train_mispredicted = row['train_mispredicted']
        train_history = row['train_history']
        train_pc = row['train_pc']

        # R7_async_reset: async reset forces outputs to 0 and clears state
        if areset:
            pht = [0] * 128
            ghr = 0
            results.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # Combinational outputs
        if predict_valid:
            # R1_predict_outputs: produce prediction and current ghr
            # R6_predict_sees_pre_train_pht: uses pre-edge pht state
            pt = predict_taken_of(predict_pc, ghr)
            ph = ghr & 0x7F
        else:
            pt = 0
            ph = 0

        results.append({'predict_taken': pt, 'predict_history': ph})

        # Sequential updates at posedge
        # R3_train_updates_pht: update PHT entry
        if train_valid:
            i = idx(train_pc, train_history)
            pht[i] = sat_update(pht[i], train_taken)

        # GHR update: training takes precedence (R5)
        if train_valid:
            if train_mispredicted:
                # R4_train_mispredicted_recovers_ghr: ghr = {train_history[5:0], train_taken}
                ghr = ((train_history << 1) | train_taken) & 0x7F
            # else: training without mispredict does not change ghr
        elif predict_valid:
            # R2_predict_updates_ghr: shift in predicted direction
            ghr = ((ghr << 1) | pt) & 0x7F

    return results
