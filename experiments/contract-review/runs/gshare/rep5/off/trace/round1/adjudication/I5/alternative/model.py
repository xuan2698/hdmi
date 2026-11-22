def reference(vectors):
    # State
    pht = [0] * 128  # 2-bit saturating counters
    ghr = 0          # 7-bit global history register

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

        # R7_async_reset: asynchronous active-high reset
        if areset:
            pht = [0] * 128
            ghr = 0
            outputs.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # Compute prediction outputs (same cycle, before any state update)
        predict_taken = 0
        predict_history = 0
        if predict_valid:
            # R1_predict_outputs: produce predicted direction and history used
            predict_history = ghr
            # R6_predict_sees_pre_train_pht: when train_valid, index using train_history
            if train_valid:
                idx = (predict_pc ^ train_history) & 0x7F
            else:
                idx = (predict_pc ^ ghr) & 0x7F
            predict_taken = 1 if pht[idx] >= 2 else 0

        outputs.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # State updates at posedge
        # R3_train_pht_update: train PHT
        if train_valid:
            tidx = (train_pc ^ train_history) & 0x7F
            if train_taken:
                if pht[tidx] < 3:
                    pht[tidx] += 1
            else:
                if pht[tidx] > 0:
                    pht[tidx] -= 1

        # GHR update: training takes precedence over prediction
        if train_valid:
            # R4_train_mispredict_ghr_recover: recover GHR on mispredict
            if train_mispredicted:
                ghr = ((train_history << 1) | train_taken) & 0x7F
            # R5_train_priority_over_predict_ghr: training takes precedence
        elif predict_valid:
            # R2_predict_ghr_update: update GHR for predicted branch
            ghr = ((ghr << 1) | predict_taken) & 0x7F

    return outputs
