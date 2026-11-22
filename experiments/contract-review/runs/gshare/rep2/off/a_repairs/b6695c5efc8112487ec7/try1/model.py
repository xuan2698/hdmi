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

        # R2_predict: combinational prediction
        # R3_predict_no_valid: when predict_valid=0, predict_taken=0, predict_history=current ghr
        if predict_valid == 1:
            idx = (predict_pc ^ ghr) & 0x7F
            cnt = pht[idx]
            predict_taken = 1 if cnt >= 2 else 0
            predict_history = ghr
        else:
            predict_taken = 0
            predict_history = ghr

        outputs.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Compute next state (posedge updates)
        next_ghr = ghr
        next_pht = list(pht)

        # R6_pht_train: update PHT on train_valid
        if train_valid == 1:
            tidx = (train_pc ^ train_history) & 0x7F
            cnt = next_pht[tidx]
            if train_taken == 1:
                if cnt < 3:
                    cnt += 1
            else:
                if cnt > 0:
                    cnt -= 1
            next_pht[tidx] = cnt

        # R5_ghr_update_train_mispredicted / R7_train_priority_over_predict
        if train_valid == 1 and train_mispredicted == 1:
            # Recover ghr to state immediately after mispredicting branch
            next_ghr = ((train_history << 1) | train_taken) & 0x7F
        elif predict_valid == 1:
            # R4_ghr_update_predict
            next_ghr = ((ghr << 1) | predict_taken) & 0x7F

        ghr = next_ghr
        pht = next_pht

    return outputs
