def reference(vectors):
    # State
    ghr = 0
    pht = [0] * 128  # 2-bit saturating counters, init 0

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

        # R1_reset: asynchronous active-high reset
        if areset == 1:
            ghr = 0
            pht = [0] * 128
            outputs.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # Compute combinational outputs
        if predict_valid == 1:
            # R2_predict: predict using pc XOR ghr
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
        # R5_ghr_update_train_mispredicted / R7_train_priority_over_predict
        # R6_pht_train
        if train_valid == 1:
            # Train PHT
            idx = (train_pc & 0x7F) ^ (train_history & 0x7F)
            counter = pht[idx]
            if train_taken == 1:
                if counter < 3:
                    counter += 1
            else:
                if counter > 0:
                    counter -= 1
            pht[idx] = counter

            if train_mispredicted == 1:
                # R5/R7: recover ghr to state after mispredicting branch
                # state immediately after branch completes = train_history shifted left with train_taken
                ghr = ((train_history << 1) | train_taken) & 0x7F
            # If not mispredicted, ghr unchanged by training
        elif predict_valid == 1:
            # R4_ghr_update_predict: shift in predicted direction
            ghr = ((ghr << 1) | predict_taken) & 0x7F

    return outputs
