def reference(vectors):
    # State
    pht = [1] * 128  # 2-bit saturating counters, init to 1 (weakly not-taken)
    ghr = 0  # 7-bit global history register

    results = []

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

        # Asynchronous active-high reset
        if areset:
            pht = [1] * 128
            ghr = 0
            results.append({'predict_taken': 0, 'predict_history': 0})
            continue

        # ---- Combinational outputs (based on current state, before edge) ----
        predict_taken = 0
        predict_history = 0
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            predict_taken = 1 if pht[idx] >= 2 else 0
            predict_history = ghr & 0x7F

        # ---- Compute next state ----
        next_pht = list(pht)
        next_ghr = ghr

        # Training update to PHT (applied at edge)
        if train_valid:
            tidx = (train_pc ^ train_history) & 0x7F
            c = next_pht[tidx]
            if train_taken:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            next_pht[tidx] = c

        # GHR next-state logic
        if train_valid and train_mispredicted:
            # Training (misprediction recovery) takes precedence
            next_ghr = ((train_history << 1) | train_taken) & 0x7F
        elif predict_valid:
            # Shift in predicted direction
            next_ghr = ((ghr << 1) | predict_taken) & 0x7F
        # else: hold

        # Commit state at positive edge
        pht = next_pht
        ghr = next_ghr

        results.append({
            'predict_taken': predict_taken & 1,
            'predict_history': predict_history & 0x7F,
        })

    return results
