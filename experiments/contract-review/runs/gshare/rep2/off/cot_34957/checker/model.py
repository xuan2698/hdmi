def reference(vectors):
    # State
    ghr = 0
    pht = [0] * 128  # 2-bit saturating counters, init 0

    out = []

    for row in vectors:
        # Read inputs (defaults if missing)
        areset = row.get('areset', 0)
        predict_valid = row.get('predict_valid', 0)
        predict_pc = row.get('predict_pc', 0)
        train_valid = row.get('train_valid', 0)
        train_taken = row.get('train_taken', 0)
        train_mispredicted = row.get('train_mispredicted', 0)
        train_history = row.get('train_history', 0)
        train_pc = row.get('train_pc', 0)

        # Asynchronous reset
        if areset:
            ghr = 0
            pht = [0] * 128
            out.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # Combinational outputs (pre-edge state)
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            ctr = pht[idx]
            predict_taken = 1 if ctr >= 2 else 0
            predict_history = ghr & 0x7F
        else:
            predict_taken = 0
            predict_history = 0

        out.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Sequential updates at posedge
        # Training takes precedence for GHR
        if train_valid:
            # Update PHT
            idx = (train_pc ^ train_history) & 0x7F
            ctr = pht[idx]
            if train_taken:
                if ctr < 3:
                    ctr += 1
            else:
                if ctr > 0:
                    ctr -= 1
            pht[idx] = ctr

            if train_mispredicted:
                # Recover GHR to state after mispredicting branch
                ghr = ((train_history << 1) | train_taken) & 0x7F
            else:
                # Normal training: still update GHR? Spec says only recover on mispredict.
                # But prediction also updates GHR. If both, training takes precedence.
                # If only training (no prediction), does GHR update? Spec: prediction updates GHR.
                # Training without mispredict doesn't update GHR per spec.
                pass
        elif predict_valid:
            # Update GHR for predicted branch (assume taken=predicted direction)
            ghr = ((ghr << 1) | predict_taken) & 0x7F

    return out
