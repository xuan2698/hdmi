def reference(vectors):
    # State
    pht = [0] * 128          # 2-bit saturating counters
    ghr = 0                  # 7-bit global history register

    out = []

    def idx(pc, hist):
        return (pc ^ hist) & 0x7F

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

        # R7_async_reset: async active-high reset forces outputs to 0
        if areset:
            pht = [0] * 128
            ghr = 0
            out.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # Compute combinational prediction outputs (R1_predict_outputs)
        # R6_predict_sees_pre_train_pht: prediction reads PHT before training update.
        # Per chosen interpretation, predict_history reflects post-train GHR
        # when same-cycle training recovery occurs.
        if predict_valid:
            pidx = idx(predict_pc, ghr)
            counter = pht[pidx]
            predict_taken = 1 if counter >= 2 else 0
            # Determine predict_history value
            if train_valid and train_mispredicted:
                # R6 chosen interpretation: post-train GHR after recovery
                predict_history = ((train_history << 1) | train_taken) & 0x7F
            else:
                predict_history = ghr
        else:
            predict_taken = 0
            predict_history = 0

        out.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Sequential updates at posedge
        # R3_train_updates_pht: update PHT entry for trained branch
        if train_valid:
            tidx = idx(train_pc, train_history)
            if train_taken:
                pht[tidx] = sat_inc(pht[tidx])
            else:
                pht[tidx] = sat_dec(pht[tidx])

        # GHR update: training takes precedence over prediction (R5)
        if train_valid:
            if train_mispredicted:
                # R4_train_mispredicted_recovers_ghr: recover GHR to state
                # immediately after the mispredicting branch completes.
                ghr = ((train_history << 1) | train_taken) & 0x7F
            else:
                # Training without misprediction: GHR unchanged
                pass
        elif predict_valid:
            # R2_predict_updates_ghr: shift in predicted direction
            ghr = ((ghr << 1) | predict_taken) & 0x7F

    return out
