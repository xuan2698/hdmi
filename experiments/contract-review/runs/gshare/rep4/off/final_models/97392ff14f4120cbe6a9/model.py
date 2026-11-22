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
        train_taken = vec.get('train_taken', 0) & 1
        train_mispredicted = vec.get('train_mispredicted', 0) & 1
        train_history = vec.get('train_history', 0) & 0x7F
        train_pc = vec.get('train_pc', 0) & 0x7F

        # R6_async_reset: asynchronous active-high reset clears GHR and PHT
        if areset:
            pht = [0] * 128
            ghr = 0
            results.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # R1_predict_outputs: combinational read of PHT and GHR before edge update
        # Prediction sees pre-training PHT state (training only modifies at posedge)
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            counter = pht[idx]
            predict_taken = 1 if counter >= 2 else 0
            predict_history = ghr
        else:
            predict_taken = 0
            predict_history = 0

        results.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Compute next-state updates (posedge)
        new_pht = list(pht)
        new_ghr = ghr

        # R3_train_pht_update: PHT entry at (train_pc xor train_history) updated toward train_taken
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

        # R4_train_mispredict_ghr_recover / R5_train_precedence_over_predict:
        # training GHR recovery wins over prediction GHR shift
        if train_valid and train_mispredicted:
            # Restore GHR to state immediately after mispredicting branch:
            # train_history with train_taken appended (shift in taken bit)
            new_ghr = ((train_history << 1) | train_taken) & 0x7F
        elif predict_valid:
            # R2_predict_ghr_update: GHR updated for predicted branch
            # Shift in predicted direction (spec doesn't specify; use predicted taken)
            new_ghr = ((ghr << 1) | predict_taken) & 0x7F

        pht = new_pht
        ghr = new_ghr

    return results
