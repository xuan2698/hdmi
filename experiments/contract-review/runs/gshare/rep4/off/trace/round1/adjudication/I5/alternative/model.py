def reference(vectors):
    # State
    pht = [0] * 128  # 2-bit saturating counters
    ghr = 0          # 7-bit global history register

    out = []

    for row in vectors:
        areset = row.get('areset', 0)
        predict_valid = row.get('predict_valid', 0)
        predict_pc = row.get('predict_pc', 0) & 0x7F
        train_valid = row.get('train_valid', 0)
        train_taken = row.get('train_taken', 0) & 1
        train_mispredicted = row.get('train_mispredicted', 0) & 1
        train_history = row.get('train_history', 0) & 0x7F
        train_pc = row.get('train_pc', 0) & 0x7F

        # R6_async_reset: asynchronous active-high reset clears GHR and PHT
        if areset:
            pht = [0] * 128
            ghr = 0
            out.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # R1_predict_outputs: combinational read of PHT and GHR
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            counter = pht[idx]
            predict_taken = 1 if counter >= 2 else 0
            predict_history = ghr
        else:
            predict_taken = 0
            predict_history = 0

        out.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Compute next state (posedge updates)
        new_pht = list(pht)
        new_ghr = ghr

        # R3_train_pht_update: train PHT entry toward train_taken
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

        # R4_train_mispredict_ghr_recover / R5_train_precedence_over_predict
        if train_valid and train_mispredicted:
            # GHR restored to train_history shifted with train_taken
            new_ghr = ((train_history << 1) | train_taken) & 0x7F
        elif predict_valid:
            # R2_predict_ghr_update: GHR <= {GHR[5:0], predict_taken}
            new_ghr = ((ghr << 1) | predict_taken) & 0x7F

        pht = new_pht
        ghr = new_ghr

    return out
