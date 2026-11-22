def reference(vectors):
    # State
    pht = [0] * 128  # 2-bit saturating counters
    ghr = 0          # 7-bit global history register

    outputs = []

    for v in vectors:
        areset = v.get('areset', 0)
        predict_valid = v.get('predict_valid', 0)
        predict_pc = v.get('predict_pc', 0)
        train_valid = v.get('train_valid', 0)
        train_taken = v.get('train_taken', 0)
        train_mispredicted = v.get('train_mispredicted', 0)
        train_history = v.get('train_history', 0)
        train_pc = v.get('train_pc', 0)

        # R7_async_reset: asynchronous active-high reset
        if areset:
            pht = [0] * 128
            ghr = 0
            outputs.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # R1_predict_outputs: combinational prediction using current ghr
        # R6_predict_sees_pre_train_pht: prediction uses PHT state before training
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            counter = pht[idx]
            predict_taken = 1 if counter >= 2 else 0
            predict_history = ghr
        else:
            predict_taken = 0
            predict_history = 0

        outputs.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Compute next state (posedge updates)
        next_pht = list(pht)
        next_ghr = ghr

        # R3_train_updates_pht: train PHT
        if train_valid:
            tidx = (train_pc ^ train_history) & 0x7F
            c = next_pht[tidx]
            if train_taken:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            next_pht[tidx] = c

        # R4_train_mispredicted_recovers_ghr / R5_train_priority_over_predict_ghr
        if train_valid:
            if train_mispredicted:
                # recover ghr to state after mispredicting branch
                next_ghr = ((train_history << 1) | train_taken) & 0x7F
            # else: training without mispredict does not change ghr
        elif predict_valid:
            # R2_predict_updates_ghr: update ghr for predicted branch
            next_ghr = ((ghr << 1) | predict_taken) & 0x7F

        pht = next_pht
        ghr = next_ghr

    return outputs
