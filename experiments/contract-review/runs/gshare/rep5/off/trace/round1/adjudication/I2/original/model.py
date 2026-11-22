def reference(vectors):
    # State
    pht = [0] * 128  # 2-bit saturating counters
    ghr = 0          # 7-bit global history register

    results = []

    for vec in vectors:
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
            results.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # Compute prediction outputs (combinational, same cycle)
        # R1_predict_outputs: when predict_valid, output predicted direction and ghr
        # R6_predict_sees_pre_train_pht: prediction uses PHT state before training update
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            counter = pht[idx]
            predict_taken = 1 if counter >= 2 else 0
            predict_history = ghr
        else:
            predict_taken = 0
            predict_history = 0

        results.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Sequential updates at posedge
        # R3_train_pht_update: train_valid updates PHT
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

        # GHR update priority: training > prediction
        # R4_train_mispredict_ghr_recover: mispredicted training recovers ghr
        # R5_train_priority_over_predict_ghr: training takes precedence
        # R2_predict_ghr_update: prediction updates ghr when no training
        if train_valid:
            if train_mispredicted:
                # Recover ghr to state immediately after mispredicting branch
                # train_history is the history used for the branch; after branch completes,
                # ghr = (train_history << 1 | train_taken) & 0x7F
                ghr = ((train_history << 1) | train_taken) & 0x7F
            else:
                # Non-mispredicted training: ghr already reflects correct path; no change
                pass
        elif predict_valid:
            # R2: update ghr for predicted branch
            ghr = ((ghr << 1) | predict_taken) & 0x7F

    return results
