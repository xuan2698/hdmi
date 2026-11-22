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

        # Compute combinational outputs (before posedge updates)
        if predict_valid == 1:
            # R2_predict: index = pc XOR ghr, read PHT
            idx = (predict_pc ^ ghr) & 0x7F
            counter = pht[idx]
            # 2-bit counter: MSB is prediction (0=not taken, 1=taken)
            predict_taken = (counter >> 1) & 1
            predict_history = ghr
        else:
            # R3_predict_no_valid: predict_taken=0, predict_history=current ghr
            predict_taken = 0
            predict_history = ghr

        outputs.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Posedge updates
        # R6_pht_train: update PHT on train_valid
        if train_valid == 1:
            idx = (train_pc ^ train_history) & 0x7F
            c = pht[idx]
            if train_taken == 1:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            pht[idx] = c

        # R5_ghr_update_train_mispredicted / R7_train_priority_over_predict
        if train_valid == 1 and train_mispredicted == 1:
            # Training takes precedence; load train_history directly
            ghr = train_history & 0x7F
        elif predict_valid == 1:
            # R4_ghr_update_predict: shift right, insert predicted direction at MSB
            ghr = ((ghr >> 1) | (predict_taken << 6)) & 0x7F

    return outputs
