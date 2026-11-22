def reference(vectors):
    # State: pht 128 entries of 2-bit counters, ghr 7-bit
    # Counter encoding: 0=00 (strongly not taken), 1=01 (weakly not taken),
    # 2=10 (weakly taken), 3=11 (strongly taken)
    # predict_taken = MSB of counter (counter >> 1) & 1  [R1 candidate interpretation]
    pht = [0] * 128
    ghr = 0

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

        # R7_async_reset: asynchronous active-high reset
        if areset:
            pht = [0] * 128
            ghr = 0
            results.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # R1_predict_outputs: combinational prediction using current state
        # R6_predict_sees_pre_train_pht: prediction uses pre-train PHT state
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            counter = pht[idx]
            # R1 candidate: predict_taken is MSB of 2-bit counter
            predict_taken = (counter >> 1) & 1
            predict_history = ghr
        else:
            predict_taken = 0
            predict_history = 0

        results.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Compute next state (posedge updates)
        new_pht = list(pht)
        new_ghr = ghr

        # R3_train_updates_pht: update PHT on training
        if train_valid:
            idx = (train_pc ^ train_history) & 0x7F
            counter = new_pht[idx]
            if train_taken:
                if counter < 3:
                    counter += 1
            else:
                if counter > 0:
                    counter -= 1
            new_pht[idx] = counter

        # R4_train_mispredicted_recovers_ghr: recover GHR on misprediction
        # R5_train_priority_over_predict_ghr: training takes precedence over prediction
        if train_valid:
            if train_mispredicted:
                # Recover to state immediately after mispredicting branch
                # train_history is the history used for the branch; after branch completes,
                # shift in actual outcome
                new_ghr = ((train_history << 1) | train_taken) & 0x7F
            # If not mispredicted, GHR is not modified by training
        elif predict_valid:
            # R2_predict_updates_ghr: update GHR for predicted branch
            # Use predicted direction
            new_ghr = ((ghr << 1) | predict_taken) & 0x7F

        pht = new_pht
        ghr = new_ghr

    return results
