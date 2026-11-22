def reference(vectors):
    # State
    pht = [0] * 128          # 2-bit saturating counters
    ghr = 0                  # 7-bit global history register

    def idx(pc, hist):
        return (pc ^ hist) & 0x7F

    def sat_inc(v):
        return v + 1 if v < 3 else 3

    def sat_dec(v):
        return v - 1 if v > 0 else 0

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

        # R7_async_reset: async active-high reset forces outputs to 0
        if areset:
            pht = [0] * 128
            ghr = 0
            results.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # R1_predict_outputs / R6_predict_sees_pre_train_pht:
        # combinational prediction uses current PHT and current GHR
        # (training effects only visible next cycle)
        if predict_valid:
            i = idx(predict_pc, ghr)
            predict_taken = 1 if pht[i] >= 2 else 0
            predict_history = ghr & 0x7F
        else:
            predict_taken = 0
            predict_history = ghr & 0x7F

        results.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Sequential updates at posedge
        # R3_train_updates_pht: train updates PHT
        if train_valid:
            ti = idx(train_pc, train_history)
            if train_taken:
                pht[ti] = sat_inc(pht[ti])
            else:
                pht[ti] = sat_dec(pht[ti])

        # R5_train_priority_over_predict_ghr: training takes precedence for GHR
        if train_valid:
            if train_mispredicted:
                # R4_train_mispredicted_recovers_ghr: recover GHR to post-branch state
                ghr = ((train_history << 1) | (train_taken & 1)) & 0x7F
            # else: training without misprediction does not modify GHR
        elif predict_valid:
            # R2_predict_updates_ghr: predicted branch updates GHR
            ghr = ((ghr << 1) | (predict_taken & 1)) & 0x7F

    return results
