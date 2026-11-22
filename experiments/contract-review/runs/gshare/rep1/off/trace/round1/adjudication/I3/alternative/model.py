def reference(vectors):
    # State
    ghr = 0
    pht = [0] * 128  # 2-bit saturating counters, init 0

    out = []

    for row in vectors:
        # Apply mid changes? The contract says mid changes occur AFTER sampling,
        # before the other edge, and are carried to the start of the next row.
        # We handle mid by processing it at the start of the next row iteration.
        # Since vectors are given as rows, we treat each row's inputs as the
        # values driven before the sampled edge. Mid changes are not explicitly
        # provided in the vector format here, so we ignore them.

        areset = row.get('areset', 0)
        predict_valid = row.get('predict_valid', 0)
        predict_pc = row.get('predict_pc', 0)
        train_valid = row.get('train_valid', 0)
        train_taken = row.get('train_taken', 0)
        train_mispredicted = row.get('train_mispredicted', 0)
        train_history = row.get('train_history', 0)
        train_pc = row.get('train_pc', 0)

        # R8_async_reset: asynchronous active-high reset
        if areset:
            ghr = 0
            pht = [0] * 128
            out.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # Combinational outputs (before posedge)
        # R1_predict_outputs: when predict_valid==1, produce prediction
        # R2_predict_no_valid: when predict_valid==0, outputs are zero (assumed)
        # R7_predict_sees_pre_train_pht: prediction sees PHT state before training
        if predict_valid:
            idx = (predict_pc & 0x7F) ^ (ghr & 0x7F)
            counter = pht[idx]
            predict_taken = 1 if counter >= 2 else 0
            predict_history = ghr & 0x7F
        else:
            predict_taken = 0
            predict_history = 0

        out.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Posedge updates
        # R4_train_pht_update: train PHT
        if train_valid:
            idx = (train_pc & 0x7F) ^ (train_history & 0x7F)
            counter = pht[idx]
            if train_taken:
                if counter < 3:
                    counter += 1
            else:
                if counter > 0:
                    counter -= 1
            pht[idx] = counter

        # R5_train_mispredict_ghr_recover: recover GHR on mispredict
        # R6_train_priority_over_predict_ghr: training takes precedence
        # R3_ghr_update_predict: update GHR for predicted branch
        if train_valid and train_mispredicted:
            # Recover GHR to state immediately after mispredicting branch
            # The branch history after the branch completes: shift in taken bit
            ghr = ((train_history << 1) | (train_taken & 1)) & 0x7F
        elif predict_valid:
            # Update GHR for predicted branch (shift in predicted direction)
            ghr = ((ghr << 1) | (predict_taken & 1)) & 0x7F

    return out
