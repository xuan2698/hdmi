def reference(vectors):
    # State
    ghr = 0
    pht = [0] * 128  # 2-bit saturating counters, reset to 0

    outputs = []

    for vec in vectors:
        areset = vec.get('areset', 0)
        predict_valid = vec.get('predict_valid', 0)
        predict_pc = vec.get('predict_pc', 0)
        train_valid = vec.get('train_valid', 0)
        train_taken = vec.get('train_taken', 0)
        train_mispredicted = vec.get('train_mispredicted', 0)
        train_history = vec.get('train_history', 0)
        train_pc = vec.get('train_pc', 0)

        # R8_async_reset: asynchronous active-high reset
        if areset:
            ghr = 0
            pht = [0] * 128
            outputs.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # R1_predict_outputs: combinational prediction using current ghr and pht
        # R7_predict_sees_pre_train_pht: prediction sees PHT before training update
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            counter = pht[idx]
            predict_taken = 1 if counter >= 2 else 0
            predict_history = ghr & 0x7F
        else:
            # R2_predict_no_valid: zero when predict_valid == 0
            predict_taken = 0
            predict_history = 0

        outputs.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Sequential updates at posedge
        # R4_train_pht_update: train PHT
        if train_valid:
            idx = (train_pc ^ train_history) & 0x7F
            counter = pht[idx]
            if train_taken:
                if counter < 3:
                    counter += 1
            else:
                if counter > 0:
                    counter -= 1
            pht[idx] = counter

        # R5_train_mispredict_ghr_recover and R6_train_priority_over_predict_ghr
        if train_valid and train_mispredicted:
            ghr = train_history & 0x7F
        elif predict_valid:
            # R3_ghr_update_predict: update ghr for predicted branch
            ghr = ((ghr << 1) | predict_taken) & 0x7F

    return outputs
