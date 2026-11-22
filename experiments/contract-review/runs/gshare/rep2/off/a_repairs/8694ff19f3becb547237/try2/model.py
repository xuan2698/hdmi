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

        # Compute combinational outputs
        if predict_valid == 1:
            # R2_predict: produce prediction using current ghr
            idx = (predict_pc & 0x7F) ^ (ghr & 0x7F)
            counter = pht[idx]
            predict_taken = 1 if counter >= 2 else 0
            predict_history = ghr & 0x7F
        else:
            # R3_predict_no_valid: assumed predict_taken=0, predict_history=current ghr
            predict_taken = 0
            predict_history = ghr & 0x7F

        outputs.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Sequential updates at posedge
        # R6_pht_train: update PHT on training
        if train_valid == 1:
            tidx = (train_pc & 0x7F) ^ (train_history & 0x7F)
            c = pht[tidx]
            if train_taken == 1:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            pht[tidx] = c

        # R5_ghr_update_train_mispredicted / R7_train_priority_over_predict
        if train_valid == 1 and train_mispredicted == 1:
            # Recover ghr to state after mispredicting branch: shift in actual outcome
            ghr = ((train_history << 1) | train_taken) & 0x7F
        elif predict_valid == 1 and train_valid == 0:
            # R4_ghr_update_predict: shift in predicted direction
            ghr = ((ghr << 1) | predict_taken) & 0x7F
        # If train_valid==1 and not mispredicted: no ghr change (training doesn't update ghr)

    return outputs
