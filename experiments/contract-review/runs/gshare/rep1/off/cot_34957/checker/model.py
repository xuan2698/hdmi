def reference(vectors):
    # State
    ghr = 0
    pht = [0] * 128  # 2-bit saturating counters, init 0

    out = []

    for row in vectors:
        # Read inputs (values driven before the sampled edge)
        areset = row.get('areset', 0)
        predict_valid = row.get('predict_valid', 0)
        predict_pc = row.get('predict_pc', 0)
        train_valid = row.get('train_valid', 0)
        train_taken = row.get('train_taken', 0)
        train_mispredicted = row.get('train_mispredicted', 0)
        train_history = row.get('train_history', 0)
        train_pc = row.get('train_pc', 0)

        # Asynchronous active-high reset: outputs reflect reset state
        if areset:
            # Reset dominates; outputs are from reset state
            predict_taken = 0
            predict_history = 0
            # Apply reset to state (asynchronous)
            ghr = 0
            pht = [0] * 128
            out.append({'predict_taken': predict_taken, 'predict_history': predict_history})
            continue

        # Prediction read (pre-edge state)
        if predict_valid:
            pred_index = (predict_pc ^ ghr) & 0x7F
            counter = pht[pred_index]
            predict_taken = (counter >> 1) & 1
            predict_history = ghr
        else:
            predict_taken = 0
            predict_history = 0

        # Compute next state (applied at posedge)
        new_ghr = ghr
        new_pht = list(pht)

        # Training update to PHT (uses train_pc ^ train_history)
        if train_valid:
            train_index = (train_pc ^ train_history) & 0x7F
            c = new_pht[train_index]
            if train_taken:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            new_pht[train_index] = c

        # GHR update: training (mispredicted) takes precedence over prediction
        if train_valid and train_mispredicted:
            new_ghr = ((train_history << 1) | train_taken) & 0x7F
        elif predict_valid:
            new_ghr = ((ghr << 1) | predict_taken) & 0x7F

        # Commit state
        ghr = new_ghr
        pht = new_pht

        out.append({'predict_taken': predict_taken, 'predict_history': predict_history})

    return out
