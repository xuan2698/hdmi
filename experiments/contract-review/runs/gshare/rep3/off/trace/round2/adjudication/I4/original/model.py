def reference(vectors):
    # State
    pht = [0] * 128  # 2-bit saturating counters
    ghr = 0          # 7-bit global history register

    def sat_inc(v):
        return v + 1 if v < 3 else 3

    def sat_dec(v):
        return v - 1 if v > 0 else 0

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

        # R1_predict_outputs: combinational prediction using current PHT and GHR
        # R6_predict_sees_pre_train_pht: prediction uses pre-train PHT state
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

        # R3_train_updates_pht: train PHT entry
        if train_valid:
            tidx = (train_pc ^ train_history) & 0x7F
            if train_taken:
                new_pht[tidx] = sat_inc(new_pht[tidx])
            else:
                new_pht[tidx] = sat_dec(new_pht[tidx])

        # R4_train_mispredicted_recovers_ghr: recover GHR on misprediction
        # R5_train_priority_over_predict_ghr: training takes precedence over prediction for GHR
        if train_valid:
            if train_mispredicted:
                # Recover to state immediately after mispredicting branch
                new_ghr = ((train_history << 1) | train_taken) & 0x7F
            # else: training without misprediction does not update GHR
        elif predict_valid:
            # R2_predict_updates_ghr: prediction updates GHR with predicted direction
            new_ghr = ((ghr << 1) | predict_taken) & 0x7F

        pht = new_pht
        ghr = new_ghr

    return results
