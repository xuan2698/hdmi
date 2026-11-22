def reference(vectors):
    # State
    pht = [0] * 128  # 2-bit saturating counters
    ghr = 0          # 7-bit global history register

    results = []

    for vec in vectors:
        areset = vec.get('areset', 0)
        predict_valid = vec.get('predict_valid', 0)
        predict_pc = vec.get('predict_pc', 0)
        train_valid = vec.get('train_valid', 0)
        train_taken = vec.get('train_taken', 0)
        train_mispredicted = vec.get('train_mispredicted', 0)
        train_history = vec.get('train_history', 0)
        train_pc = vec.get('train_pc', 0)

        # R6_async_reset: asynchronous active-high reset clears GHR and PHT
        if areset:
            pht = [0] * 128
            ghr = 0
            results.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # R1_predict_outputs: combinational read of PHT and GHR before edge update
        # predict_taken = PHT[index][1] (MSB of 2-bit counter)
        if predict_valid:
            idx = (predict_pc & 0x7F) ^ (ghr & 0x7F)
            predict_taken = (pht[idx] >> 1) & 1
            predict_history = ghr & 0x7F
        else:
            predict_taken = 0
            predict_history = ghr & 0x7F

        results.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Compute next state (posedge updates)
        new_pht = list(pht)
        new_ghr = ghr

        # R3_train_pht_update: PHT entry at (train_pc xor train_history) updated toward train_taken
        if train_valid:
            tidx = (train_pc & 0x7F) ^ (train_history & 0x7F)
            c = new_pht[tidx]
            if train_taken:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            new_pht[tidx] = c

        # R4_train_mispredict_ghr_recover: GHR restored to train_history shifted with train_taken
        # R5_train_precedence_over_predict: training GHR recovery wins over prediction GHR shift
        if train_valid and train_mispredicted:
            new_ghr = ((train_history << 1) | (train_taken & 1)) & 0x7F
        elif predict_valid:
            # R2_predict_ghr_update: GHR shifts in predicted direction at posedge
            new_ghr = ((ghr << 1) | (predict_taken & 1)) & 0x7F

        pht = new_pht
        ghr = new_ghr

    return results
