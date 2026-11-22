def reference(vectors):
    # State
    pht = [0] * 128          # 2-bit saturating counters
    ghr = 0                  # 7-bit global history register

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

        # R1_predict_outputs / R8_index_xor: combinational prediction
        # R6_predict_sees_pre_train_pht: prediction uses pre-train PHT state
        predict_taken = 0
        predict_history = 0
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F  # R8_index_xor
            predict_taken = 1 if pht[idx] >= 2 else 0  # R1_predict_outputs
            predict_history = ghr  # R1_predict_outputs

        outputs.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Sequential updates at posedge
        # R5_train_priority_over_predict_ghr: training takes precedence for GHR
        if train_valid:
            # R3_train_updates_pht / R9_train_index_uses_train_history
            tidx = (train_pc ^ train_history) & 0x7F
            if train_taken:
                if pht[tidx] < 3:
                    pht[tidx] += 1
            else:
                if pht[tidx] > 0:
                    pht[tidx] -= 1

            # R4_train_mispredicted_recovers_ghr
            if train_mispredicted:
                ghr = ((train_history << 1) | train_taken) & 0x7F
            else:
                # Non-mispredicted training: does not update GHR per spec
                pass
        elif predict_valid:
            # R2_predict_updates_ghr
            ghr = ((ghr << 1) | predict_taken) & 0x7F

    return outputs
