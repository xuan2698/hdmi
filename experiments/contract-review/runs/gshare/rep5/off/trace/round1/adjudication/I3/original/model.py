def reference(vectors):
    # State
    pht = [0] * 128  # 2-bit saturating counters
    ghr = 0          # 7-bit global history register

    outputs = []

    def predict_taken_for(pc, hist):
        idx = (pc ^ hist) & 0x7F
        return 1 if pht[idx] >= 2 else 0

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

        # R1_predict_outputs: predict outputs based on current state
        if predict_valid:
            pred_taken = predict_taken_for(predict_pc, ghr)
            pred_history = ghr
        else:
            pred_taken = 0
            pred_history = 0

        outputs.append({'predict_taken': pred_taken, 'predict_history': pred_history})

        # Compute next state (posedge updates)
        next_ghr = ghr
        next_pht = list(pht)

        # R3_train_pht_update: train PHT
        if train_valid:
            idx = (train_pc ^ train_history) & 0x7F
            c = next_pht[idx]
            if train_taken:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            next_pht[idx] = c

        # R4_train_mispredict_ghr_recover: recover GHR on mispredict
        # R5_train_priority_over_predict_ghr: training takes precedence
        if train_valid:
            if train_mispredicted:
                # Recover to state immediately after mispredicting branch
                next_ghr = ((train_history << 1) | train_taken) & 0x7F
            else:
                # Normal training: shift in actual outcome
                next_ghr = ((train_history << 1) | train_taken) & 0x7F
        elif predict_valid:
            # R2_predict_ghr_update: update GHR for predicted branch
            next_ghr = ((ghr << 1) | pred_taken) & 0x7F

        # R6_predict_sees_pre_train_pht: prediction already used old pht above
        pht = next_pht
        ghr = next_ghr

    return outputs
