def reference(vectors):
    # State
    pht = [0] * 128  # 2-bit saturating counters
    ghr = 0          # 7-bit global history register

    outputs = []

    for vec in vectors:
        # Read inputs
        areset = vec.get('areset', 0)
        predict_valid = vec.get('predict_valid', 0)
        predict_pc = vec.get('predict_pc', 0)
        train_valid = vec.get('train_valid', 0)
        train_taken = vec.get('train_taken', 0)
        train_mispredicted = vec.get('train_mispredicted', 0)
        train_history = vec.get('train_history', 0)
        train_pc = vec.get('train_pc', 0)

        # R7_async_reset: asynchronous active-high reset
        if areset:
            pht = [0] * 128
            ghr = 0
            outputs.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # Compute prediction outputs (combinational, based on current state)
        # R1_predict_outputs: when predict_valid, produce predicted direction and history
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            counter = pht[idx]
            # predict_taken: 1 if counter >= 2 (MSB of 2-bit counter)
            predict_taken = 1 if counter >= 2 else 0
            predict_history = ghr
        else:
            predict_taken = 0
            predict_history = 0

        # R6_predict_sees_pre_train_pht: prediction uses PHT state before training update
        # (already handled since we read pht before updating)

        outputs.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Sequential updates at posedge
        # R3_train_pht_update: update PHT counter (saturating)
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

        # GHR update logic
        # R5_train_priority_over_predict_ghr: training takes precedence over prediction
        if train_valid:
            if train_mispredicted:
                # R4_train_mispredict_ghr_recover: recover GHR to state after mispredicting branch
                # The state immediately after the branch completes = train_history with the
                # actual outcome shifted in
                ghr = ((train_history << 1) | train_taken) & 0x7F
            else:
                # Training without mispredict: shift in actual outcome
                ghr = ((train_history << 1) | train_taken) & 0x7F
        elif predict_valid:
            # R2_predict_ghr_update: update GHR for predicted branch
            ghr = ((ghr << 1) | predict_taken) & 0x7F

    return outputs
