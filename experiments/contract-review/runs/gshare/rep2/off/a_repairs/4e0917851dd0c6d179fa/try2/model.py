def reference(vectors):
    # State
    ghr = 0
    pht = [0] * 128

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

        # Compute prediction outputs (combinational, before edge updates)
        if predict_valid == 1:
            # R2_predict: index = pc XOR ghr, read PHT
            idx = (predict_pc ^ ghr) & 0x7F
            counter = pht[idx]
            # counter >= 2 means taken (2-bit saturating counter)
            predict_taken = 1 if counter >= 2 else 0
            predict_history = ghr
        else:
            # R3_predict_no_valid: assumed predict_taken=0, predict_history=current ghr
            predict_taken = 0
            predict_history = ghr

        outputs.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Edge updates (posedge)
        # R6_pht_train: update PHT on training
        if train_valid == 1:
            tidx = (train_pc ^ train_history) & 0x7F
            c = pht[tidx]
            if train_taken == 1:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            pht[tidx] = c

        # R5_ghr_update_train_mispredicted / R7_train_priority_over_predict
        if train_valid == 1 and train_mispredicted == 1:
            # Training takes precedence; load train_history directly
            ghr = train_history & 0x7F
        elif predict_valid == 1:
            # R4_ghr_update_predict: shift left, insert predicted direction at LSB
            ghr = ((ghr << 1) | predict_taken) & 0x7F

    return outputs
