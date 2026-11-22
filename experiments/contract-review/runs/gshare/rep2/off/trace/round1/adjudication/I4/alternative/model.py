def reference(vectors):
    # State
    ghr = 0
    pht = [0] * 128  # 2-bit saturating counters, init 0

    out = []

    for v in vectors:
        areset = v.get('areset', 0)
        predict_valid = v.get('predict_valid', 0)
        predict_pc = v.get('predict_pc', 0)
        train_valid = v.get('train_valid', 0)
        train_taken = v.get('train_taken', 0)
        train_mispredicted = v.get('train_mispredicted', 0)
        train_history = v.get('train_history', 0)
        train_pc = v.get('train_pc', 0)

        # R1_reset: asynchronous active-high reset -> outputs 0
        if areset:
            ghr = 0
            pht = [0] * 128
            out.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # Combinational outputs
        if predict_valid:
            # R2_predict: index = pc XOR ghr, read PHT, output MSB and current ghr
            idx = (predict_pc & 0x7F) ^ (ghr & 0x7F)
            counter = pht[idx]
            predict_taken = (counter >> 1) & 1
            predict_history = ghr & 0x7F
        else:
            # R3_predict_no_valid: assumed predict_taken=0, predict_history=current ghr
            predict_taken = 0
            predict_history = ghr & 0x7F

        out.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Sequential updates at posedge
        # R6_pht_train: train PHT (uses train_history for index)
        if train_valid:
            tidx = (train_pc & 0x7F) ^ (train_history & 0x7F)
            c = pht[tidx]
            if train_taken:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            pht[tidx] = c

        # GHR update priority:
        # R5_ghr_update_train_mispredicted (priority 1): recover ghr = (train_history<<1)|taken
        # R7_train_priority_over_predict: any train_valid suppresses prediction GHR update
        # R4_ghr_update_predict: only when train_valid==0
        if train_valid:
            if train_mispredicted:
                # R5: recover to state immediately after mispredicting branch
                ghr = ((train_history << 1) | (train_taken & 1)) & 0x7F
            # else: training without mispredict does not update GHR
        else:
            if predict_valid:
                # R4: shift in predicted direction
                ghr = ((ghr << 1) | (predict_taken & 1)) & 0x7F

    return out
