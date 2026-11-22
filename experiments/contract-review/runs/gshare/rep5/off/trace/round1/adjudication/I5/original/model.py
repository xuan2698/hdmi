def reference(vectors):
    # State
    pht = [0] * 128          # 2-bit saturating counters
    ghr = 0                  # 7-bit global history register

    out = []

    def index_of(pc, hist):
        return (pc ^ hist) & 0x7F

    def predict_taken_for(pc, hist):
        idx = index_of(pc, hist)
        # 2-bit counter: MSB is direction (>=2 taken)
        return 1 if (pht[idx] >> 1) & 1 else 0

    for row in vectors:
        areset = row.get('areset', 0)
        predict_valid = row.get('predict_valid', 0)
        predict_pc = row.get('predict_pc', 0) & 0x7F
        train_valid = row.get('train_valid', 0)
        train_taken = row.get('train_taken', 0) & 1
        train_mispredicted = row.get('train_mispredicted', 0) & 1
        train_history = row.get('train_history', 0) & 0x7F
        train_pc = row.get('train_pc', 0) & 0x7F

        # R7_async_reset: asynchronous active-high reset
        if areset:
            pht = [0] * 128
            ghr = 0
            out.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # R1_predict_outputs: same-cycle prediction outputs
        # R6_predict_sees_pre_train_pht: prediction uses pre-train PHT state
        if predict_valid:
            pred_taken = predict_taken_for(predict_pc, ghr)
            pred_history = ghr
        else:
            pred_taken = 0
            pred_history = 0

        out.append({'predict_taken': pred_taken, 'predict_history': pred_history})

        # Compute next-state updates (applied at posedge)
        new_pht = list(pht)
        new_ghr = ghr

        # R3_train_pht_update: train PHT
        if train_valid:
            idx = index_of(train_pc, train_history)
            c = new_pht[idx]
            if train_taken:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            new_pht[idx] = c

        # R4_train_mispredict_ghr_recover: recover GHR on mispredict
        # R5_train_priority_over_predict_ghr: training takes precedence over prediction
        if train_valid:
            if train_mispredicted:
                # Recover to state immediately after mispredicting branch
                new_ghr = ((train_history << 1) | train_taken) & 0x7F
            else:
                # Normal training: shift in actual outcome
                new_ghr = ((train_history << 1) | train_taken) & 0x7F
        elif predict_valid:
            # R2_predict_ghr_update: update GHR for predicted branch
            new_ghr = ((ghr << 1) | pred_taken) & 0x7F

        pht = new_pht
        ghr = new_ghr

    return out
