def reference(vectors):
    # State
    ghr = 0
    pht = [0] * 128  # 2-bit saturating counters, init 0

    out = []

    def pht_index(pc, hist):
        return (pc ^ hist) & 0x7F

    def sat_update(counter, taken):
        # 2-bit saturating counter: 0..3
        if taken:
            return counter + 1 if counter < 3 else 3
        else:
            return counter - 1 if counter > 0 else 0

    for row in vectors:
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

        # R1_predict_outputs / R2_predict_no_valid: combinational prediction
        if predict_valid:
            idx = pht_index(predict_pc, ghr)
            counter = pht[idx]
            # predict taken if MSB of 2-bit counter is 1 (counter >= 2)
            predict_taken = 1 if counter >= 2 else 0
            predict_history = ghr
        else:
            # R2: assumed held/zero -> zero
            predict_taken = 0
            predict_history = 0

        out.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Sequential updates at posedge
        # R4_train_pht_update: train PHT
        if train_valid:
            tidx = pht_index(train_pc, train_history)
            pht[tidx] = sat_update(pht[tidx], train_taken)

        # GHR update logic
        # R5_train_mispredict_ghr_recover: GHR becomes train_history (interpretation chosen)
        # R6_train_priority_over_predict_ghr: training takes precedence
        # R3_ghr_update_predict: predict updates GHR when no training mispredict
        if train_valid and train_mispredicted:
            # R5 + R6: recover GHR to train_history
            ghr = train_history & 0x7F
        elif predict_valid:
            # R3: shift in predicted direction
            ghr = ((ghr << 1) | predict_taken) & 0x7F
        # else: hold

    return out
