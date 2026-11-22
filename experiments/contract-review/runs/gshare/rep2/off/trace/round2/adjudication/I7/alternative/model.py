def reference(vectors):
    # State
    ghr = 0
    pht = [0] * 128  # 2-bit saturating counters, init 0 (weakly not-taken)

    outputs = []

    def pht_index(pc, hist):
        return (pc & 0x7F) ^ (hist & 0x7F)

    def sat_update(counter, taken):
        # 2-bit saturating counter: 0,1,2,3
        if taken:
            return min(3, counter + 1)
        else:
            return max(0, counter - 1)

    for row in vectors:
        areset = row.get('areset', 0)
        predict_valid = row.get('predict_valid', 0)
        predict_pc = row.get('predict_pc', 0)
        train_valid = row.get('train_valid', 0)
        train_taken = row.get('train_taken', 0)
        train_mispredicted = row.get('train_mispredicted', 0)
        train_history = row.get('train_history', 0)
        train_pc = row.get('train_pc', 0)

        # R1_reset: asynchronous active-high reset, visible same cycle
        if areset == 1:
            ghr = 0
            pht = [0] * 128
            outputs.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # Compute combinational prediction outputs (before any posedge updates)
        # R2_predict: predict_valid==1 -> produce prediction from current state
        # R3_predict_no_valid: predict_valid==0 -> predict_taken=0, predict_history=current ghr
        if predict_valid == 1:
            idx = pht_index(predict_pc, ghr)
            counter = pht[idx]
            predict_taken = 1 if counter >= 2 else 0
            predict_history = ghr & 0x7F
        else:
            predict_taken = 0
            predict_history = ghr & 0x7F

        outputs.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Posedge updates (next cycle visible)
        # R6_pht_train: train_valid -> update PHT entry
        if train_valid == 1:
            idx = pht_index(train_pc, train_history)
            pht[idx] = sat_update(pht[idx], train_taken)

        # GHR update logic with priority:
        # R5_ghr_update_train_mispredicted (priority 1): train_valid && train_mispredicted
        #   -> ghr = (train_history << 1) | train_taken
        # R7_train_priority_over_predict: training takes precedence over prediction
        # R4_ghr_update_predict: predict_valid && !train_valid -> ghr = (ghr << 1) | predict_taken
        if train_valid == 1 and train_mispredicted == 1:
            ghr = ((train_history << 1) | train_taken) & 0x7F
        elif predict_valid == 1 and train_valid == 0:
            ghr = ((ghr << 1) | predict_taken) & 0x7F
        # If train_valid==1 but not mispredicted: no GHR change (only PHT trained)

    return outputs
