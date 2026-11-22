def reference(vectors):
    # State
    pht = [0] * 128  # 2-bit saturating counters
    ghr = 0          # 7-bit global history register

    results = []

    for vec in vectors:
        areset = vec.get('areset', 0)
        predict_valid = vec.get('predict_valid', 0)
        predict_pc = vec.get('predict_pc', 0) & 0x7F
        train_valid = vec.get('train_valid', 0)
        train_taken = vec.get('train_taken', 0)
        train_mispredicted = vec.get('train_mispredicted', 0)
        train_history = vec.get('train_history', 0) & 0x7F
        train_pc = vec.get('train_pc', 0) & 0x7F

        # R7_async_reset: async active-high reset
        if areset:
            pht = [0] * 128
            ghr = 0
            results.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # R1_predict_outputs: combinational prediction using current ghr and pht
        # R6_predict_sees_pre_train_pht: prediction uses pht state before training edge
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

        # R3_train_updates_pht: train updates PHT
        if train_valid:
            tidx = (train_pc ^ train_history) & 0x7F
            c = new_pht[tidx]
            if train_taken:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            new_pht[tidx] = c

        # R4_train_mispredicted_recovers_ghr: recover ghr on misprediction
        # R5_train_priority_over_predict_ghr: training takes precedence over prediction for ghr
        if train_valid:
            if train_mispredicted:
                # recover to state immediately after mispredicting branch
                new_ghr = ((train_history << 1) | train_taken) & 0x7F
            # else: training without misprediction does not update ghr per spec
        elif predict_valid:
            # R2_predict_updates_ghr: prediction updates ghr
            new_ghr = ((ghr << 1) | predict_taken) & 0x7F

        pht = new_pht
        ghr = new_ghr

    return results
