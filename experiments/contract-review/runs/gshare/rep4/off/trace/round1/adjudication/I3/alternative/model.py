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
            ghr = 0
            pht = [0] * 128
            results.append({'predict_taken': 0, 'predict_history': 0})
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

        results.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Compute next state (posedge updates)
        new_ghr = ghr
        new_pht = list(pht)

        # R3_train_pht_update: PHT entry updated at posedge
        # Candidate interpretation: set directly to 2'b11 if train_taken else 2'b00
        if train_valid:
            tidx = (train_pc ^ train_history) & 0x7F
            new_pht[tidx] = 3 if train_taken else 0

        # R4_train_mispredict_ghr_recover / R5_train_precedence_over_predict
        if train_valid and train_mispredicted:
            # GHR restored to train_history shifted with train_taken
            new_ghr = ((train_history << 1) | (train_taken & 1)) & 0x7F
        elif predict_valid:
            # R2_predict_ghr_update: shift in predicted direction
            new_ghr = ((ghr << 1) | (predict_taken & 1)) & 0x7F

        ghr = new_ghr
        pht = new_pht

    return results
