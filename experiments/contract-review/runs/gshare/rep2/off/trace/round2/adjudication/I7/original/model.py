def reference(vectors):
    # State
    ghr = 0
    pht = [0] * 128  # 2-bit saturating counters, init 0

    outputs = []

    for vec in vectors:
        areset = vec['areset']
        predict_valid = vec['predict_valid']
        predict_pc = vec['predict_pc']
        train_valid = vec['train_valid']
        train_taken = vec['train_taken']
        train_mispredicted = vec['train_mispredicted']
        train_history = vec['train_history']
        train_pc = vec['train_pc']

        # R1_reset: asynchronous active-high reset
        if areset == 1:
            ghr = 0
            pht = [0] * 128
            outputs.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # Compute combinational outputs (before any posedge updates)
        if predict_valid == 1:
            # R2_predict: predict using pc XOR ghr
            idx = (predict_pc ^ ghr) & 0x7F
            counter = pht[idx]
            # 2-bit counter: MSB is prediction (>=2 means taken)
            pred_taken = 1 if counter >= 2 else 0
            pred_history = ghr
        else:
            # R3_predict_no_valid: assumed predict_taken=0, predict_history=current ghr
            pred_taken = 0
            pred_history = ghr

        outputs.append({'predict_taken': pred_taken, 'predict_history': pred_history})

        # Posedge updates
        # R6_pht_train: update PHT on training
        if train_valid == 1:
            tidx = (train_pc ^ train_history) & 0x7F
            c = pht[tidx]
            if train_taken == 1:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            pht[tidx] = c

        # GHR update priority: R5/R7 (train mispredicted) > R4 (predict)
        if train_valid == 1 and train_mispredicted == 1:
            # R5_ghr_update_train_mispredicted / R7_train_priority_over_predict
            # Recover GHR to state immediately after mispredicting branch
            # train_history is the history used for the branch; after branch completes,
            # shift in actual outcome
            ghr = ((train_history << 1) | train_taken) & 0x7F
        elif predict_valid == 1:
            # R4_ghr_update_predict: shift in predicted direction
            ghr = ((ghr << 1) | pred_taken) & 0x7F

    return outputs
