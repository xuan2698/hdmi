def reference(vectors):
    # State
    pht = [0] * 128  # 2-bit saturating counters, reset to 0 (strongly not-taken)
    ghr = 0          # 7-bit global history register

    outputs = []

    def sat_inc(v):
        return v + 1 if v < 3 else 3

    def sat_dec(v):
        return v - 1 if v > 0 else 0

    for row in vectors:
        areset = row.get('areset', 0)
        predict_valid = row.get('predict_valid', 0)
        predict_pc = row.get('predict_pc', 0) & 0x7F
        train_valid = row.get('train_valid', 0)
        train_taken = row.get('train_taken', 0)
        train_mispredicted = row.get('train_mispredicted', 0)
        train_history = row.get('train_history', 0) & 0x7F
        train_pc = row.get('train_pc', 0) & 0x7F

        # R7_async_reset: asynchronous active-high reset
        if areset:
            pht = [0] * 128
            ghr = 0
            outputs.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # R1_predict_outputs: prediction outputs based on current state (pre-edge)
        # R6_predict_sees_pre_train_pht: prediction sees PHT before training update
        if predict_valid:
            pred_idx = (predict_pc ^ ghr) & 0x7F
            pred_counter = pht[pred_idx]
            predict_taken = 1 if pred_counter >= 2 else 0
            predict_history = ghr
        else:
            predict_taken = 0
            predict_history = 0

        outputs.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Compute next state (posedge updates)
        new_pht = list(pht)
        new_ghr = ghr

        # R3_train_pht_update: train PHT
        if train_valid:
            train_idx = (train_pc ^ train_history) & 0x7F
            if train_taken:
                new_pht[train_idx] = sat_inc(new_pht[train_idx])
            else:
                new_pht[train_idx] = sat_dec(new_pht[train_idx])

        # R4_train_mispredict_ghr_recover: recover GHR on mispredict
        # R5_train_priority_over_predict_ghr: training takes precedence over prediction
        if train_valid:
            if train_mispredicted:
                # Recover GHR to state immediately after mispredicting branch
                # train_history is the history used for the branch; after branch completes,
                # shift in the actual outcome
                new_ghr = ((train_history << 1) | train_taken) & 0x7F
            # If not mispredicted, GHR is not modified by training
        elif predict_valid:
            # R2_predict_ghr_update: update GHR for predicted branch
            new_ghr = ((ghr << 1) | predict_taken) & 0x7F

        pht = new_pht
        ghr = new_ghr

    return outputs
