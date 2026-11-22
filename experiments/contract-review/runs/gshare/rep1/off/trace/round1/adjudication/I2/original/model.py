def reference(vectors):
    # State
    ghr = 0
    pht = [0] * 128  # 2-bit saturating counters, init 0

    out = []

    def sat_update(counter, taken):
        # 2-bit saturating counter update
        if taken:
            return min(3, counter + 1)
        else:
            return max(0, counter - 1)

    for row in vectors:
        # Apply mid changes: mid inputs occur AFTER sampling, before other edge,
        # carried to start of next row. We process them at end of each row.
        areset = row.get('areset', 0)
        predict_valid = row.get('predict_valid', 0)
        predict_pc = row.get('predict_pc', 0)
        train_valid = row.get('train_valid', 0)
        train_taken = row.get('train_taken', 0)
        train_mispredicted = row.get('train_mispredicted', 0)
        train_history = row.get('train_history', 0)
        train_pc = row.get('train_pc', 0)

        # R8_async_reset: asynchronous active-high reset
        if areset:
            ghr = 0
            pht = [0] * 128
            out.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # R1_predict_outputs: combinational prediction outputs
        # R7_predict_sees_pre_train_pht: prediction sees PHT before training update
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            counter = pht[idx]
            predict_taken = 1 if counter >= 2 else 0
            predict_history = ghr & 0x7F
        else:
            # R2_predict_no_valid: assume zero when no valid prediction
            predict_taken = 0
            predict_history = 0

        out.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Compute next state (posedge updates)
        next_ghr = ghr
        next_pht = list(pht)

        # R4_train_pht_update: train PHT
        if train_valid:
            tidx = (train_pc ^ train_history) & 0x7F
            next_pht[tidx] = sat_update(next_pht[tidx], train_taken)

        # R5_train_mispredict_ghr_recover: recover GHR on mispredict
        # R6_train_priority_over_predict_ghr: training takes precedence over prediction
        if train_valid and train_mispredicted:
            # GHR becomes train_history shifted in with actual outcome
            next_ghr = ((train_history << 1) | train_taken) & 0x7F
        elif predict_valid:
            # R3_ghr_update_predict: update GHR for predicted branch
            next_ghr = ((ghr << 1) | predict_taken) & 0x7F

        ghr = next_ghr
        pht = next_pht

    return out
