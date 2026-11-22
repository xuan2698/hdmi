def reference(vectors):
    # State
    ghr = 0
    pht = [0] * 128  # 2-bit saturating counters, init 0

    # Output registers (hold previous values when predict_valid=0 per R3 interpretation)
    out_taken = 0
    out_history = 0

    results = []

    for vec in vectors:
        areset = vec['areset']
        predict_valid = vec['predict_valid']
        predict_pc = vec['predict_pc']
        train_valid = vec['train_valid']
        train_taken = vec['train_taken']
        train_mispredicted = vec['train_mispredicted']
        train_history = vec['train_history']
        train_pc = vec['train_pc']

        # R1_reset: asynchronous active-high reset, visible same cycle
        if areset == 1:
            ghr = 0
            pht = [0] * 128
            out_taken = 0
            out_history = 0
            results.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # Combinational outputs (before posedge updates)
        # R2_predict: predict_valid=1 -> output predicted direction and current ghr
        if predict_valid == 1:
            idx = (predict_pc & 0x7F) ^ (ghr & 0x7F)
            counter = pht[idx]
            # 2-bit counter: MSB indicates taken (>=2 means taken)
            pred_taken = 1 if counter >= 2 else 0
            out_taken = pred_taken
            out_history = ghr & 0x7F
        # R3_predict_no_valid: outputs hold previous values when predict_valid=0
        # (out_taken, out_history unchanged)

        results.append({'predict_taken': out_taken, 'predict_history': out_history})

        # Posedge updates
        # R6_pht_train: train_valid=1 -> update PHT counter
        if train_valid == 1:
            idx = (train_pc & 0x7F) ^ (train_history & 0x7F)
            counter = pht[idx]
            if train_taken == 1:
                if counter < 3:
                    counter += 1
            else:
                if counter > 0:
                    counter -= 1
            pht[idx] = counter

        # GHR update priority: R5/R7 (train mispredicted) > R4 (predict)
        # R5_ghr_update_train_mispredicted / R7_train_priority_over_predict
        if train_valid == 1 and train_mispredicted == 1:
            # Recover ghr to state immediately after mispredicting branch
            # train_history is the ghr value used for the branch; shift in actual outcome
            ghr = ((train_history << 1) | train_taken) & 0x7F
        # R4_ghr_update_predict: predict_valid=1 and no training
        elif predict_valid == 1 and train_valid == 0:
            idx = (predict_pc & 0x7F) ^ (ghr & 0x7F)
            counter = pht[idx]
            pred_taken = 1 if counter >= 2 else 0
            ghr = ((ghr << 1) | pred_taken) & 0x7F

    return results
