def reference(vectors):
    # State
    pht = [0] * 128          # 2-bit saturating counters, init 0
    ghr = 0                  # 7-bit global history register

    results = []

    for v in vectors:
        areset = v.get('areset', 0)
        predict_valid = v.get('predict_valid', 0)
        predict_pc = v.get('predict_pc', 0) & 0x7F
        train_valid = v.get('train_valid', 0)
        train_taken = v.get('train_taken', 0) & 1
        train_mispredicted = v.get('train_mispredicted', 0) & 1
        train_history = v.get('train_history', 0) & 0x7F
        train_pc = v.get('train_pc', 0) & 0x7F

        if areset:
            pht = [0] * 128
            ghr = 0
            results.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # Combinational prediction (uses current state, before any updates)
        predict_taken = 0
        predict_history = 0
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            predict_taken = 1 if pht[idx] >= 2 else 0
            predict_history = ghr

        # Compute next state
        next_pht = list(pht)
        next_ghr = ghr

        # Prediction updates GHR (unless training overrides)
        if predict_valid:
            next_ghr = ((ghr << 1) | predict_taken) & 0x7F

        # Training takes precedence
        if train_valid:
            idx = (train_pc ^ train_history) & 0x7F
            c = next_pht[idx]
            if train_taken:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            next_pht[idx] = c

            if train_mispredicted:
                next_ghr = ((train_history << 1) | train_taken) & 0x7F

        pht = next_pht
        ghr = next_ghr

        results.append({'predict_taken': predict_taken, 'predict_history': predict_history})

    return results
