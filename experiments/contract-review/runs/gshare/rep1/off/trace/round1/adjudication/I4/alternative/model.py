def reference(vectors):
    # State
    ghr = 0
    pht = [0] * 128  # 2-bit saturating counters, init 0

    outputs = []

    def sat_inc(v):
        return v + 1 if v < 3 else 3

    def sat_dec(v):
        return v - 1 if v > 0 else 0

    for row in vectors:
        areset = row.get('areset', 0)
        predict_valid = row.get('predict_valid', 0)
        predict_pc = row.get('predict_pc', 0)
        train_valid = row.get('train_valid', 0)
        train_taken = row.get('train_taken', 0)
        train_mispredicted = row.get('train_mispredicted', 0)
        train_history = row.get('train_history', 0)
        train_pc = row.get('train_pc', 0)

        # R8_async_reset: async active-high reset
        if areset:
            ghr = 0
            pht = [0] * 128
            outputs.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # R1_predict_outputs / R2_predict_no_valid: combinational outputs
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            counter = pht[idx]
            predict_taken = 1 if counter >= 2 else 0
            predict_history = ghr & 0x7F
        else:
            # R2: assumed zero when no prediction
            predict_taken = 0
            predict_history = 0

        outputs.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Compute next state (posedge updates)
        new_ghr = ghr
        new_pht = list(pht)

        # R4_train_pht_update: train PHT
        if train_valid:
            tidx = (train_pc ^ train_history) & 0x7F
            if train_taken:
                new_pht[tidx] = sat_inc(new_pht[tidx])
            else:
                new_pht[tidx] = sat_dec(new_pht[tidx])

        # R5_train_mispredict_ghr_recover / R6_train_priority_over_predict_ghr
        if train_valid and train_mispredicted:
            # Recover GHR to state after mispredicting branch
            new_ghr = ((train_history << 1) | train_taken) & 0x7F
        elif predict_valid:
            # R3_ghr_update_predict: update GHR for predicted branch
            new_ghr = ((ghr << 1) | predict_taken) & 0x7F

        ghr = new_ghr
        pht = new_pht

    return outputs
