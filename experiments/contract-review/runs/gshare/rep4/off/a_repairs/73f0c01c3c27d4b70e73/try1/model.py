def reference(vectors):
    # State: PHT 128 entries of 2-bit counters, GHR 7-bit
    # Selected interpretations (to match contract examples):
    #  - R6: reset -> GHR=0, PHT all 2'b00
    #  - R5: any train_valid=1 takes precedence over prediction GHR update
    #  - R2: GHR shifts in predicted direction when predict_valid and not train_valid
    #  - R3: PHT index uses train_history (not current GHR)
    pht = [0] * 128
    ghr = 0
    out = []

    for row in vectors:
        areset = row.get('areset', 0)
        predict_valid = row.get('predict_valid', 0)
        predict_pc = row.get('predict_pc', 0) & 0x7F
        train_valid = row.get('train_valid', 0)
        train_taken = row.get('train_taken', 0) & 1
        train_mispredicted = row.get('train_mispredicted', 0) & 1
        train_history = row.get('train_history', 0) & 0x7F
        train_pc = row.get('train_pc', 0) & 0x7F

        # R6_async_reset: asynchronous active-high reset
        if areset:
            ghr = 0
            pht = [0] * 128
            out.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # R1_predict_outputs: combinational read of PHT and GHR
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            predict_taken = 1 if pht[idx] >= 2 else 0
            predict_history = ghr
        else:
            predict_taken = 0
            predict_history = ghr

        out.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Compute next state (posedge updates)
        new_pht = list(pht)
        new_ghr = ghr

        # R3_train_pht_update: PHT entry at (train_pc xor train_history) updated toward train_taken
        if train_valid:
            tidx = (train_pc ^ train_history) & 0x7F
            c = new_pht[tidx]
            if train_taken:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            new_pht[tidx] = c

        # R4_train_mispredict_ghr_recover and R5_train_precedence_over_predict
        if train_valid:
            if train_mispredicted:
                # R4: restore GHR to train_history
                new_ghr = train_history
            # R5: any train_valid takes precedence over prediction GHR update
        elif predict_valid:
            # R2_predict_ghr_update: shift in predicted direction
            new_ghr = ((ghr << 1) | predict_taken) & 0x7F

        pht = new_pht
        ghr = new_ghr

    return out
