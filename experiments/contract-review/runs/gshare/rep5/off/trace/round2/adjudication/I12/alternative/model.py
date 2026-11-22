def reference(vectors):
    # State
    pht = [0] * 128  # 2-bit saturating counters, reset to 0 (R7)
    ghr = 0          # 7-bit global history register (R7)

    outputs = []

    for v in vectors:
        areset = v['areset']
        predict_valid = v['predict_valid']
        predict_pc = v['predict_pc']
        train_valid = v['train_valid']
        train_taken = v['train_taken']
        train_mispredicted = v['train_mispredicted']
        train_history = v['train_history']
        train_pc = v['train_pc']

        # R7_async_reset: asynchronous active-high reset
        if areset:
            pht = [0] * 128
            ghr = 0
            outputs.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # Compute prediction outputs (same cycle, pre-update PHT) (R1, R6)
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            counter = pht[idx]
            predict_taken = 1 if counter >= 2 else 0
            # R1 interpretation: predict_history outputs GHR after shifting in predicted direction
            predict_history = ((ghr << 1) | predict_taken) & 0x7F
        else:
            predict_taken = 0
            predict_history = 0

        outputs.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Sequential updates at posedge
        # R3_train_pht_update: train PHT
        if train_valid:
            tidx = (train_pc ^ train_history) & 0x7F
            c = pht[tidx]
            if train_taken:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            pht[tidx] = c

        # GHR update: training takes precedence over prediction (R5)
        if train_valid:
            if train_mispredicted:
                # R4_train_mispredict_ghr_recover: recover GHR to state after mispredicting branch
                ghr = ((train_history << 1) | train_taken) & 0x7F
            # else: training without mispredict does not update GHR per spec
        elif predict_valid:
            # R2_predict_ghr_update: update GHR for predicted branch
            ghr = ((ghr << 1) | predict_taken) & 0x7F

    return outputs
