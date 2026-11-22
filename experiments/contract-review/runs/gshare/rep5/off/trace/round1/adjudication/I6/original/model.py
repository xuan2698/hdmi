def reference(vectors):
    # State
    pht = [0] * 128          # 2-bit saturating counters
    ghr = 0                  # 7-bit global history register

    outputs = []

    def idx(pc, hist):
        return (pc ^ hist) & 0x7F

    def predict_taken_for(pc, hist):
        return 1 if pht[idx(pc, hist)] >= 2 else 0

    for row in vectors:
        # R7_async_reset: asynchronous active-high reset dominates
        if row.get('areset', 0) == 1:
            pht = [0] * 128
            ghr = 0
            outputs.append({'predict_taken': 0, 'predict_history': 0})
            continue

        pv = row.get('predict_valid', 0)
        ppc = row.get('predict_pc', 0) & 0x7F
        tv = row.get('train_valid', 0)
        tt = row.get('train_taken', 0)
        tm = row.get('train_mispredicted', 0)
        th = row.get('train_history', 0) & 0x7F
        tpc = row.get('train_pc', 0) & 0x7F

        # R1_predict_outputs: same-cycle outputs based on current state
        # R6_predict_sees_pre_train_pht: prediction uses pre-edge PHT
        if pv:
            pt = predict_taken_for(ppc, ghr)
            ph = ghr
        else:
            pt = 0
            ph = 0
        outputs.append({'predict_taken': pt, 'predict_history': ph})

        # Compute next-state values (applied at posedge)
        new_pht = list(pht)
        new_ghr = ghr

        # R3_train_pht_update: update PHT counter for trained branch
        if tv:
            i = idx(tpc, th)
            c = new_pht[i]
            if tt:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            new_pht[i] = c

        # R4_train_mispredict_ghr_recover / R5_train_priority_over_predict_ghr
        if tv:
            if tm:
                # recover GHR to state immediately after mispredicting branch
                new_ghr = ((th << 1) | (tt & 1)) & 0x7F
            else:
                # training without mispredict: no GHR change specified
                pass
        elif pv:
            # R2_predict_ghr_update: shift in predicted direction
            new_ghr = ((ghr << 1) | (pt & 1)) & 0x7F

        pht = new_pht
        ghr = new_ghr

    return outputs
